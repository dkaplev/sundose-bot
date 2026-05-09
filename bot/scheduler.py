from __future__ import annotations

import logging
from datetime import datetime, timedelta

import pytz
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.keyboards import morning_notification_kb
from bot.messages import AREA_NOTIFICATION, BADGE_NAMES, days_word, t
from core.dosage import adjust_for_clouds, calculate_exposure
from core.oracle import build_oracle_message, fetch_weekly_uv
from core.personas import get_persona
from core.uv import fetch_uv_data, format_window, get_avg_cloud_cover_in_window, get_peak_uv, parse_uv_window
from db import crud

logger = logging.getLogger(__name__)

_sent_reminders: set[tuple[int, str]] = set()


# ── Morning notifications ──────────────────────────────────────────────────

async def send_morning_notifications(bot: Bot, session_factory: async_sessionmaker[AsyncSession]):
    now_utc = datetime.now(pytz.UTC)
    async with session_factory() as session:
        users = await crud.get_active_users(session)

    for user in users:
        if not user.timezone or not user.lat:
            continue
        try:
            user_tz = pytz.timezone(user.timezone)
            now_local = now_utc.astimezone(user_tz)
            if now_local.hour != user.notify_hour:
                continue
            await _send_morning_for_user(bot, session_factory, user, now_local)
        except Exception as e:
            logger.error("Morning notification error for %s: %s", user.telegram_id, e)


async def _send_morning_for_user(bot: Bot, session_factory, user, now_local: datetime):
    lang = user.language
    date_str = now_local.date().isoformat()
    try:
        data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        window = parse_uv_window(data)

        if not window:
            await bot.send_message(user.telegram_id, t(lang, "winter_notification", city=user.city))
            return

        uv = get_peak_uv(data)
        base_min = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
        cloud = get_avg_cloud_cover_in_window(data)
        minutes, cloudy = adjust_for_clouds(base_min, cloud)

        async with session_factory() as session:
            fresh_user = await crud.get_user(session, user.telegram_id)
            tip, tier2_new, tier3_new = await crud.get_next_tip(session, fresh_user)

        persona = get_persona(user.streak, lang)
        dw = days_word(lang, user.streak)
        area_text = AREA_NOTIFICATION[lang].get(user.exposed_area, "")
        best_hour = window[0][0] + 1

        text = t(
            lang, "morning_notification",
            city=user.city, window=format_window(window), uv=f"{uv:.0f}",
            minutes=minutes, best_time=f"{best_hour:02d}:00",
            area_text=area_text, streak=user.streak, days_word=dw,
            persona=persona, tip=tip,
        )
        if cloudy and cloud:
            text += t(lang, "cloud_warning", cloud=cloud, minutes=minutes, base=base_min)

        await bot.send_message(user.telegram_id, text, reply_markup=morning_notification_kb(lang, date_str), parse_mode="HTML")

        if tier2_new:
            await bot.send_message(user.telegram_id, t(lang, "tier2_unlock"), parse_mode="HTML")
        if tier3_new:
            await bot.send_message(user.telegram_id, t(lang, "tier3_unlock"), parse_mode="HTML")

        await _check_duel_status(bot, session_factory, user, now_local.date())

    except Exception as e:
        logger.error("Morning notification failed for %s: %s", user.telegram_id, e)


# ── Duel daily check ───────────────────────────────────────────────────────

async def _check_duel_status(bot: Bot, session_factory, user, today):
    async with session_factory() as session:
        duel = await crud.get_active_duel(session, user.telegram_id)
        if not duel or not duel.started_at:
            return

        days_in = (today - duel.started_at).days + 1
        if days_in > 7:
            return

        my_streak = duel.challenger_streak if duel.challenger == user.telegram_id else duel.opponent_streak
        opp_streak = duel.opponent_streak if duel.challenger == user.telegram_id else duel.challenger_streak
        lang = user.language

        if opp_streak < days_in - 1:
            winner_id = await crud.resolve_duel(session, duel, loser_id=duel.opponent if duel.challenger == user.telegram_id else duel.challenger)
            if winner_id == user.telegram_id:
                await bot.send_message(user.telegram_id, t(lang, "duel_victory"), parse_mode="HTML")
            else:
                await bot.send_message(user.telegram_id, t(lang, "duel_defeat"))


# ── Window reminders ───────────────────────────────────────────────────────

async def send_window_reminders(bot: Bot, session_factory: async_sessionmaker[AsyncSession]):
    now_utc = datetime.now(pytz.UTC)
    async with session_factory() as session:
        users = await crud.get_active_users(session)

    for user in users:
        if not user.timezone or not user.lat:
            continue
        try:
            user_tz = pytz.timezone(user.timezone)
            now_local = now_utc.astimezone(user_tz)
            date_str = now_local.date().isoformat()
            reminder_key = (user.telegram_id, date_str)
            if reminder_key in _sent_reminders:
                continue

            data = await fetch_uv_data(user.lat, user.lon, user.timezone)
            window = parse_uv_window(data)
            if not window:
                continue

            window_start = now_local.replace(hour=window[0][0], minute=0, second=0, microsecond=0)
            minutes_until = (window_start - now_local).total_seconds() / 60

            if 20 <= minutes_until <= 40:
                uv = get_peak_uv(data)
                cloud = get_avg_cloud_cover_in_window(data)
                base_min = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
                minutes, _ = adjust_for_clouds(base_min, cloud)
                await bot.send_message(user.telegram_id, t(user.language, "reminder_30", minutes=minutes))
                _sent_reminders.add(reminder_key)
                if len(_sent_reminders) > 10000:
                    _sent_reminders.clear()

        except Exception as e:
            logger.error("Reminder error for %s: %s", user.telegram_id, e)


# ── One-shot reminder (from /now button) ──────────────────────────────────

def _schedule_one_reminder(scheduler: AsyncIOScheduler, user_id: int, lang: str, city: str, run_at: datetime):
    async def _send(bot_ref):
        try:
            await bot_ref.send_message(user_id, f"⏰ {'Твоё напоминание!' if lang == 'ru' else 'Your reminder!'} ☀️")
        except Exception:
            pass

    scheduler.add_job(
        _send,
        trigger=DateTrigger(run_date=run_at),
        args=[scheduler._jobstores["default"]],
        id=f"oneshot_{user_id}",
        replace_existing=True,
        misfire_grace_time=120,
    )


# ── Evening forecast ───────────────────────────────────────────────────────

async def send_evening_forecasts(bot: Bot, session_factory: async_sessionmaker[AsyncSession]):
    now_utc = datetime.now(pytz.UTC)
    async with session_factory() as session:
        users = await crud.get_active_users(session)

    for user in users:
        if not user.evening_notify or not user.timezone or not user.lat:
            continue
        try:
            user_tz = pytz.timezone(user.timezone)
            now_local = now_utc.astimezone(user_tz)
            if now_local.hour != 21:
                continue

            await _send_evening_forecast(bot, user)
        except Exception as e:
            logger.error("Evening forecast error for %s: %s", user.telegram_id, e)


async def _send_evening_forecast(bot: Bot, user):
    lang = user.language
    try:
        tomorrow = datetime.utcnow().date() + timedelta(days=1)
        data = await fetch_weekly_uv(user.lat, user.lon, user.timezone)

        times = data["hourly"]["time"]
        uvs = data["hourly"]["uv_index"]
        clouds = data["hourly"].get("cloud_cover", [None] * len(times))

        tomorrow_str = tomorrow.isoformat()
        tomorrow_hours = [
            (int(t[11:13]), uv, c)
            for t, uv, c in zip(times, uvs, clouds)
            if t.startswith(tomorrow_str)
        ]

        window_hours = [(h, uv) for h, uv, _ in tomorrow_hours if uv and uv >= 3]
        peak_uv = max((uv for _, uv, _ in tomorrow_hours if uv), default=0.0)
        avg_cloud = sum(c for _, _, c in tomorrow_hours if c is not None) / max(1, sum(1 for _, _, c in tomorrow_hours if c is not None))

        if window_hours:
            win_str = f"{window_hours[0][0]:02d}:00 – {window_hours[-1][0] + 1:02d}:00"
            best_h = max(window_hours, key=lambda x: x[1])[0]
            comment_key = "forecast_comment_excellent" if peak_uv >= 9 else "forecast_comment_good" if peak_uv >= 6 else "forecast_comment_normal"
            text = t(lang, "evening_forecast", city=user.city, window=win_str, uv=f"{peak_uv:.0f}", best_time=f"{best_h:02d}:00", cloud=avg_cloud, comment=t(lang, comment_key))
        else:
            text = t(lang, "evening_forecast_weak", city=user.city, uv=peak_uv, cloud=avg_cloud)

        await bot.send_message(user.telegram_id, text, parse_mode="HTML")
    except Exception as e:
        logger.error("Evening forecast send failed for %s: %s", user.telegram_id, e)


# ── Weekly oracle (Sunday 10:00) ───────────────────────────────────────────

async def send_weekly_oracle(bot: Bot, session_factory: async_sessionmaker[AsyncSession]):
    now_utc = datetime.now(pytz.UTC)
    async with session_factory() as session:
        users = await crud.get_active_users(session)

    for user in users:
        if not user.timezone or not user.lat:
            continue
        try:
            user_tz = pytz.timezone(user.timezone)
            now_local = now_utc.astimezone(user_tz)
            if now_local.weekday() != 6 or now_local.hour != 10:
                continue

            await _send_oracle(bot, user)
        except Exception as e:
            logger.error("Oracle error for %s: %s", user.telegram_id, e)


async def _send_oracle(bot: Bot, user):
    lang = user.language
    try:
        data = await fetch_weekly_uv(user.lat, user.lon, user.timezone)
        times = data["hourly"]["time"]
        uvs = data["hourly"]["uv_index"]

        daily_peaks: dict[int, float] = {}
        for t_str, uv in zip(times, uvs):
            if uv is None:
                continue
            day_of_week = datetime.fromisoformat(t_str[:10]).weekday()
            daily_peaks[day_of_week] = max(daily_peaks.get(day_of_week, 0), uv)

        if not daily_peaks:
            return

        best_day = max(daily_peaks, key=lambda d: daily_peaks[d])
        peak_uv = daily_peaks[best_day]
        good_days = sum(1 for v in daily_peaks.values() if v >= 3)

        window_hours = [(int(t_str[11:13]), uv) for t_str, uv in zip(times, uvs) if uv and uv >= 3]
        win_str = f"{window_hours[0][0]:02d}:00 – {window_hours[-1][0] + 1:02d}:00" if window_hours else "–"
        minutes = calculate_exposure(user.skin_type or 3, user.exposed_area, peak_uv) if peak_uv >= 3 else 0

        text = build_oracle_message(lang, user.city, peak_uv, best_day, win_str, minutes, good_days)
        await bot.send_message(user.telegram_id, text)
    except Exception as e:
        logger.error("Oracle send failed for %s: %s", user.telegram_id, e)


# ── Weekly stats (Sunday 20:00) ────────────────────────────────────────────

async def send_weekly_stats(bot: Bot, session_factory: async_sessionmaker[AsyncSession]):
    now_utc = datetime.now(pytz.UTC)
    async with session_factory() as session:
        users = await crud.get_active_users(session)

    for user in users:
        if not user.timezone:
            continue
        try:
            user_tz = pytz.timezone(user.timezone)
            now_local = now_utc.astimezone(user_tz)
            if now_local.weekday() != 6 or now_local.hour != 20:
                continue

            async with session_factory() as session:
                stats = await crud.get_weekly_stats(session, user.telegram_id)

            lang = user.language
            persona = get_persona(user.streak, lang)
            dw = days_word(lang, user.streak)
            text = t(lang, "weekly_stats", city=user.city or "–", sessions=stats["sessions"], total_iu=stats["total_iu"], streak=user.streak, days_word=dw, persona=persona)
            await bot.send_message(user.telegram_id, text, parse_mode="HTML")
        except Exception as e:
            logger.error("Weekly stats error for %s: %s", user.telegram_id, e)


# ── Setup ──────────────────────────────────────────────────────────────────

def setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot, session_factory):
    scheduler.add_job(send_morning_notifications, "cron", minute=0, args=[bot, session_factory], id="morning", replace_existing=True)
    scheduler.add_job(send_window_reminders, "interval", minutes=10, args=[bot, session_factory], id="reminders", replace_existing=True)
    scheduler.add_job(send_evening_forecasts, "cron", minute=0, args=[bot, session_factory], id="evening", replace_existing=True)
    scheduler.add_job(send_weekly_oracle, "cron", minute=0, args=[bot, session_factory], id="oracle", replace_existing=True)
    scheduler.add_job(send_weekly_stats, "cron", minute=0, args=[bot, session_factory], id="weekly_stats", replace_existing=True)
