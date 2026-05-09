from __future__ import annotations

import logging
from datetime import datetime, timedelta

import pytz
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.keyboards import morning_notification_kb
from bot.messages import AREA_NOTIFICATION, t
from core.dosage import adjust_for_clouds, calculate_exposure
from core.uv import (
    fetch_uv_data,
    format_window,
    get_avg_cloud_cover_in_window,
    get_peak_uv,
    parse_uv_window,
)
from db import crud

logger = logging.getLogger(__name__)

# In-memory set to prevent duplicate reminders: {(user_id, date_str)}
_sent_reminders: set[tuple[int, str]] = set()


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
            logger.error("Morning notification error for user %s: %s", user.telegram_id, e)


async def _send_morning_for_user(bot: Bot, session_factory, user, now_local: datetime):
    lang = user.language
    date_str = now_local.date().isoformat()

    try:
        data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        window = parse_uv_window(data)

        if not window:
            text = t(lang, "winter_notification", city=user.city)
            await bot.send_message(user.telegram_id, text)
            return

        uv = get_peak_uv(data)
        base_minutes = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
        cloud = get_avg_cloud_cover_in_window(data)
        minutes, cloudy = adjust_for_clouds(base_minutes, cloud)

        win_str = format_window(window)
        best_hour = window[0][0] + 1
        best_time = f"{best_hour:02d}:00"
        area_text = AREA_NOTIFICATION[lang].get(user.exposed_area, "")

        async with session_factory() as session:
            tip, _ = await crud.get_next_tip(session, user)

        text = t(
            lang,
            "morning_notification",
            city=user.city,
            window=win_str,
            uv=f"{uv:.0f}",
            minutes=minutes,
            best_time=best_time,
            area_text=area_text,
            tip=tip,
        )

        if cloudy and cloud:
            text += t(lang, "cloud_warning", cloud=cloud, minutes=minutes, base=base_minutes)

        await bot.send_message(
            user.telegram_id,
            text,
            reply_markup=morning_notification_kb(lang, date_str),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error("Failed to send morning notification for %s: %s", user.telegram_id, e)


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

            window_start_hour = window[0][0]
            window_start = now_local.replace(hour=window_start_hour, minute=0, second=0, microsecond=0)
            minutes_until = (window_start - now_local).total_seconds() / 60

            if 20 <= minutes_until <= 40:
                lang = user.language
                uv = get_peak_uv(data)
                base_minutes = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
                cloud = get_avg_cloud_cover_in_window(data)
                minutes, _ = adjust_for_clouds(base_minutes, cloud)

                text = t(lang, "reminder_30", minutes=minutes)
                await bot.send_message(user.telegram_id, text)
                _sent_reminders.add(reminder_key)

                if len(_sent_reminders) > 10000:
                    _sent_reminders.clear()

        except Exception as e:
            logger.error("Reminder error for user %s: %s", user.telegram_id, e)


def setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot, session_factory):
    scheduler.add_job(
        send_morning_notifications,
        trigger="cron",
        minute=0,
        args=[bot, session_factory],
        id="morning_notifications",
        replace_existing=True,
    )
    scheduler.add_job(
        send_window_reminders,
        trigger="interval",
        minutes=10,
        args=[bot, session_factory],
        id="window_reminders",
        replace_existing=True,
    )
