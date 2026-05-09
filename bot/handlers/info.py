from __future__ import annotations

from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages import AREA_NOTIFICATION, days_word, t
from core.dosage import calculate_exposure
from core.uv import fetch_uv_data, format_window, get_avg_cloud_cover_in_window, get_peak_uv, parse_uv_window
from db import crud

router = Router()


@router.message(Command("status"))
async def cmd_status(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    if not user or not user.city:
        await message.answer("Сначала настрой бота: /start")
        return

    lang = user.language
    header = t(lang, "status_header", city=user.city)

    try:
        data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        window = parse_uv_window(data)
        if window:
            uv = get_peak_uv(data)
            minutes = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
            win_str = format_window(window)
            best_hour = window[0][0] + 1
            best_time = f"{best_hour:02d}:00"
            area_text = AREA_NOTIFICATION[lang].get(user.exposed_area, "")
            body = t(lang, "status_window", window=win_str, uv=f"{uv:.0f}", minutes=minutes, best_time=best_time, area_text=area_text)
        else:
            body = t(lang, "status_winter")
    except Exception:
        body = t(lang, "error_uv")

    await message.answer(header + body, parse_mode="HTML")


@router.message(Command("streak"))
async def cmd_streak(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    if not user:
        await message.answer("Сначала настрой бота: /start")
        return
    lang = user.language
    dw = days_word(lang, user.streak)
    await message.answer(t(lang, "streak_info", streak=user.streak, days_word=dw), parse_mode="HTML")


@router.message(Command("tip"))
async def cmd_tip(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    if not user:
        await message.answer("Сначала настрой бота: /start")
        return
    lang = user.language
    tip, _ = await crud.get_next_tip(session, user)
    await message.answer(t(lang, "tip_message", tip=tip), parse_mode="HTML")


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
    new_streak = await crud.apply_went_out(session, user, log_date)
    dw = days_word(lang, new_streak)
    text = t(lang, "went_out_response", streak=new_streak, days_word=dw)
    await call.message.edit_text(text, parse_mode="HTML")
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
        text = t(lang, "streak_reset")
    else:
        text = t(lang, "skipped_response", streak=new_streak, days_word=dw)

    await call.message.edit_text(text)
    await call.answer()
