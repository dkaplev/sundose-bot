from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages import t
from db import crud

router = Router()


@router.message(Command("duel"))
async def cmd_duel(message: Message, session: AsyncSession):
    user = await crud.get_user(session, message.from_user.id)
    if not user or not user.city:
        await message.answer("Сначала настрой бота: /start")
        return

    lang = user.language
    active = await crud.get_active_duel(session, message.from_user.id)
    if active:
        from datetime import datetime
        if active.started_at:
            days_in = (datetime.utcnow().date() - active.started_at).days + 1
            my_streak = active.challenger_streak if active.challenger == message.from_user.id else active.opponent_streak
            opp_streak = active.opponent_streak if active.challenger == message.from_user.id else active.challenger_streak
            await message.answer(t(lang, "duel_status", day=days_in, my_streak=my_streak, opp_streak=opp_streak))
        return

    duel = await crud.create_duel(session, message.from_user.id)
    bot_username = (await message.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start=duel_{duel.token}"
    await message.answer(t(lang, "duel_created", link=link), parse_mode="HTML")
