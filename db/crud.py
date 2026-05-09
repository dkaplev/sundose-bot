from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DailyLog, User


async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, telegram_id: int, language: str = "ru") -> User:
    user = User(telegram_id=telegram_id, language=language)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_or_create_user(session: AsyncSession, telegram_id: int) -> tuple[User, bool]:
    user = await get_user(session, telegram_id)
    if user:
        return user, False
    user = await create_user(session, telegram_id)
    return user, True


async def update_user(session: AsyncSession, telegram_id: int, **kwargs) -> None:
    await session.execute(
        update(User).where(User.telegram_id == telegram_id).values(**kwargs)
    )
    await session.commit()


async def get_active_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).where(User.active == True, User.city != None))
    return list(result.scalars().all())


async def log_daily(
    session: AsyncSession,
    user_id: int,
    log_date: date,
    went_out: bool,
    uv_at_time: float | None = None,
    recommended_min: int | None = None,
) -> None:
    entry = DailyLog(
        user_id=user_id,
        log_date=log_date,
        went_out=went_out,
        uv_at_time=uv_at_time,
        recommended_min=recommended_min,
        logged_at=datetime.utcnow(),
    )
    session.add(entry)
    await session.commit()


async def apply_went_out(session: AsyncSession, user: User, log_date: date) -> int:
    if user.last_out == log_date:
        return user.streak

    new_streak = user.streak + 1
    await update_user(session, user.telegram_id, streak=new_streak, last_out=log_date)
    await log_daily(session, user.telegram_id, log_date, went_out=True)
    return new_streak


async def apply_skipped(session: AsyncSession, user: User, log_date: date) -> int:
    from datetime import timedelta

    if user.last_out is None or (log_date - user.last_out).days > 1:
        await update_user(session, user.telegram_id, streak=0)
        await log_daily(session, user.telegram_id, log_date, went_out=False)
        return 0

    await log_daily(session, user.telegram_id, log_date, went_out=False)
    return user.streak


async def get_next_tip(session: AsyncSession, user: User) -> tuple[str, int]:
    from core.tips import TIPS

    tip = TIPS[user.tip_index % len(TIPS)]
    next_index = (user.tip_index + 1) % len(TIPS)
    await update_user(session, user.telegram_id, tip_index=next_index)
    return tip, next_index
