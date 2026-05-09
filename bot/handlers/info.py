from __future__ import annotations

from datetime import date, datetime

import pytz
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from bot import keyboards as kb
from bot.messages import AREA_NOTIFICATION, BADGE_NAMES, days_word, t
from core.dosage import adjust_for_clouds, calculate_exposure
from core.personas import days_to_next_level, get_persona
from core.uv import fetch_uv_data, format_window, get_avg_cloud_cover_in_window, get_peak_uv, parse_uv_window
from db import crud

router = Router()


def _build_went_out_text(lang: str, streak: int, persona: str, iu: int | None) -> str:
    dw = days_word(lang, streak)
    next_days = days_to_next_level(streak)
    next_line = (
        t(lang, "next_level_line", days=next_days, days_word=days_word(lang, next_days))
        if next_days else t(lang, "max_level_line")
    )
    iu_line = t(lang, "iu_line", iu=iu) if iu else ""
    return t(lang, "went_out_response", streak=streak, days_word=dw, persona=persona, next_level_line=next_line, iu_line=iu_line)


@router.message(Command("status"))
async def cmd_status(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    if not user or not user.city:
        await message.answer("Сначала настрой бота: /start")
        return
    await _send_status(message, user)


@router.message(F.text.in_({"☀️ Проверить сейчас", "☀️ Check now"}))
@router.message(Command("now"))
async def cmd_now(message: Message, session: AsyncSession, scheduler: AsyncIOScheduler):
    user = await crud.get_user(session, message.from_user.id)
    if not user or not user.city:
        await message.answer("Сначала настрой бота: /start")
        return

    lang = user.language
    try:
        data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        window = parse_uv_window(data)
        all_uvs = data["hourly"]["uv_index"]
        all_times = data["hourly"]["time"]

        user_tz = pytz.timezone(user.timezone)
        now_local = datetime.now(pytz.UTC).astimezone(user_tz)
        current_hour = now_local.hour

        current_uv = next((uv for t_str, uv in zip(all_times, all_uvs) if int(t_str[11:13]) == current_hour), 0.0) or 0.0

        cloud = get_avg_cloud_cover_in_window(data)
        minutes = calculate_exposure(user.skin_type or 3, user.exposed_area, current_uv or 3.0)
        minutes, _ = adjust_for_clouds(minutes, cloud)
        area_text = AREA_NOTIFICATION[lang].get(user.exposed_area, "")
        date_str = now_local.date().isoformat()

        active_now = any(h == current_hour for h, _ in window)

        if active_now and current_uv >= 3:
            end_hour = window[-1][0] + 1 if window else current_hour + 1
            remaining_min = (end_hour - current_hour) * 60
            remaining = f"{remaining_min // 60} ч {remaining_min % 60} мин" if lang == "ru" else f"{remaining_min // 60}h {remaining_min % 60}m"
            text = t(lang, "now_active", city=user.city, uv=f"{current_uv:.1f}", remaining=remaining, minutes=minutes, area_text=area_text)
            await message.answer(text, reply_markup=kb.now_active_kb(lang, date_str), parse_mode="HTML")
        else:
            future_window = [(h, uv) for h, uv in window if h > current_hour]
            if future_window:
                next_h = future_window[0][0]
                window_msg = t(lang, "now_window_later", time=f"{next_h:02d}:00")
            else:
                next_h = window[0][0] if window else 11
                window_msg = t(lang, "now_window_none", time=f"{next_h:02d}:00")
            text = t(lang, "now_inactive", city=user.city, uv=f"{current_uv:.1f}", window_msg=window_msg)
            await message.answer(text, reply_markup=kb.now_inactive_kb(lang), parse_mode="HTML")

    except Exception:
        await message.answer(t(lang, "error_uv"))


@router.callback_query(F.data == "remind:30")
async def cb_remind_30(call: CallbackQuery, session: AsyncSession, scheduler: AsyncIOScheduler):
    user = await crud.get_user(session, call.from_user.id)
    if not user:
        await call.answer()
        return
    lang = user.language
    user_tz = pytz.timezone(user.timezone or "UTC")
    now_local = datetime.now(pytz.UTC).astimezone(user_tz)
    remind_at_utc = datetime.now(pytz.UTC).replace(tzinfo=None)
    from datetime import timedelta
    remind_at_utc = datetime.utcnow() + timedelta(minutes=30)
    remind_time_local = (datetime.now(pytz.UTC) + timedelta(minutes=30)).astimezone(user_tz)

    from bot.scheduler import _schedule_one_reminder
    _schedule_one_reminder(scheduler, call.from_user.id, lang, user.city or "", remind_at_utc)

    await call.message.edit_text(t(lang, "remind_scheduled", time=remind_time_local.strftime("%H:%M")))
    await call.answer()


@router.callback_query(F.data == "remind:window")
async def cb_remind_window(call: CallbackQuery, session: AsyncSession, scheduler: AsyncIOScheduler):
    user = await crud.get_user(session, call.from_user.id)
    if not user or not user.lat:
        await call.answer()
        return
    lang = user.language
    try:
        data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        window = parse_uv_window(data)
        if not window:
            await call.answer("No window today")
            return
        user_tz = pytz.timezone(user.timezone or "UTC")
        now_local = datetime.now(pytz.UTC).astimezone(user_tz)
        window_start = now_local.replace(hour=window[0][0], minute=0, second=0, microsecond=0)
        from datetime import timedelta
        remind_at_local = window_start - timedelta(minutes=30)
        remind_at_utc = remind_at_local.astimezone(pytz.UTC).replace(tzinfo=None)

        if remind_at_utc > datetime.utcnow():
            from bot.scheduler import _schedule_one_reminder
            _schedule_one_reminder(scheduler, call.from_user.id, lang, user.city or "", remind_at_utc)
            await call.message.edit_text(t(lang, "remind_scheduled", time=remind_at_local.strftime("%H:%M")))
        else:
            await call.answer("Window already started or too close")
    except Exception:
        await call.answer()


@router.message(Command("streak"))
async def cmd_streak(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    if not user:
        await message.answer("Сначала настрой бота: /start")
        return
    lang = user.language
    persona = get_persona(user.streak, lang)
    dw = days_word(lang, user.streak)
    next_days = days_to_next_level(user.streak)
    next_line = (
        t(lang, "next_level_line", days=next_days, days_word=days_word(lang, next_days))
        if next_days else t(lang, "max_level_line")
    )
    await message.answer(t(lang, "streak_info", streak=user.streak, days_word=dw, persona=persona, next_level_line=next_line), parse_mode="HTML")


@router.message(Command("tip"))
async def cmd_tip(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    if not user:
        await message.answer("Сначала настрой бота: /start")
        return
    lang = user.language
    tip, tier2_new, tier3_new = await crud.get_next_tip(session, user)
    await message.answer(t(lang, "tip_message", tip=tip), parse_mode="HTML")
    if tier2_new:
        await message.answer(t(lang, "tier2_unlock"), parse_mode="HTML")
    if tier3_new:
        await message.answer(t(lang, "tier3_unlock"), parse_mode="HTML")


@router.message(Command("winter"))
async def cmd_winter(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    lang = user.language if user else "ru"
    await message.answer(t(lang, "winter_info"), parse_mode="HTML")


@router.message(Command("about"))
async def cmd_about(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    lang = user.language if user else "ru"
    await message.answer(t(lang, "about_text"), parse_mode="HTML")


@router.message(Command("stop"))
async def cmd_stop(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    lang = user.language if user else "ru"
    await crud.update_user(session, message.from_user.id, active=False)
    await message.answer(t(lang, "stopped"))


@router.callback_query(F.data.startswith("went_out:"))
async def cb_went_out(call: CallbackQuery, session: AsyncSession):
    date_str = call.data.split(":")[1]
    log_date = date.fromisoformat(date_str)
    user = await crud.get_user(session, call.from_user.id)
    if not user:
        await call.answer()
        return

    lang = user.language
    user_tz = pytz.timezone(user.timezone or "UTC")
    now_local = datetime.now(pytz.UTC).astimezone(user_tz)

    try:
        uv_data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        uv = get_peak_uv(uv_data)
        window = parse_uv_window(uv_data)
        cloud = get_avg_cloud_cover_in_window(uv_data)
        base_min = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
        minutes, _ = adjust_for_clouds(base_min, cloud)
    except Exception:
        uv, minutes = None, None

    new_streak = await crud.apply_went_out(session, user, log_date, uv=uv, minutes=minutes, session_hour=now_local.hour)

    badge_slug = await crud.check_streak_badge(session, call.from_user.id, new_streak)
    persona = get_persona(new_streak, lang)

    from core.iu import estimate_iu
    iu = estimate_iu(user.skin_type or 3, user.exposed_area, uv or 6.0, minutes or 20) if uv else None

    text = _build_went_out_text(lang, new_streak, persona, iu)
    await call.message.edit_text(text, parse_mode="HTML")

    if badge_slug:
        badge_name = BADGE_NAMES[lang].get(badge_slug, badge_slug)
        await call.message.answer(t(lang, "badge_earned", badge_name=badge_name), parse_mode="HTML")

    await call.message.answer(t(lang, "alone_or_together"), reply_markup=kb.alone_or_together_kb(lang))
    await call.answer()


@router.callback_query(F.data.startswith("skipped:"))
async def cb_skipped(call: CallbackQuery, session: AsyncSession):
    date_str = call.data.split(":")[1]
    log_date = date.fromisoformat(date_str)
    user = await crud.get_user(session, call.from_user.id)
    if not user:
        await call.answer()
        return

    lang = user.language
    new_streak = await crud.apply_skipped(session, user, log_date)
    dw = days_word(lang, new_streak)

    if new_streak == 0 and (user.streak or 0) > 0:
        await call.message.edit_text(t(lang, "streak_reset"))
    else:
        await call.message.edit_text(t(lang, "skipped_response", streak=new_streak, days_word=dw))
    await call.answer()


@router.callback_query(F.data == "session:alone")
async def cb_alone(call: CallbackQuery):
    await call.message.delete()
    await call.answer()


@router.callback_query(F.data == "session:together")
async def cb_together(call: CallbackQuery, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    lang = user.language if user else "ru"
    bot_username = (await call.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start=duo_{call.from_user.id}"
    await call.message.edit_text(t(lang, "share_duo_link", link=link), parse_mode="HTML")
    await call.answer()


async def _send_status(message: Message, user):
    lang = user.language
    header = t(lang, "status_header", city=user.city)
    try:
        data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        window = parse_uv_window(data)
        if window:
            uv = get_peak_uv(data)
            cloud = get_avg_cloud_cover_in_window(data)
            base_min = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
            minutes, _ = adjust_for_clouds(base_min, cloud)
            best_hour = window[0][0] + 1
            area_text = AREA_NOTIFICATION[lang].get(user.exposed_area, "")
            body = t(lang, "status_window", window=format_window(window), uv=f"{uv:.0f}", minutes=minutes, best_time=f"{best_hour:02d}:00", area_text=area_text)
        else:
            body = t(lang, "status_winter")
    except Exception:
        body = t(lang, "error_uv")
    await message.answer(header + body, parse_mode="HTML")
