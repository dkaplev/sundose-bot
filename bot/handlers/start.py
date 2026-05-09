from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot import keyboards as kb
from bot.messages import AREA_NAMES, SKIN_NAMES, t
from core.uv import fetch_uv_data, format_window, geocode_city, get_peak_uv, get_timezone, parse_uv_window
from core.dosage import calculate_exposure
from db import crud

router = Router()


class Onboarding(StatesGroup):
    city_input = State()
    city_confirm = State()
    skin_type = State()
    exposed_area = State()
    notify_hour = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    user, created = await crud.get_or_create_user(session, message.from_user.id)
    if not created and user.city:
        lang = user.language
        await message.answer(t(lang, "already_registered"))
        return

    await state.clear()
    await message.answer(t("ru", "choose_language"), reply_markup=kb.language_kb())


@router.callback_query(F.data.startswith("lang:"))
async def cb_language(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    lang = call.data.split(":")[1]
    await crud.update_user(session, call.from_user.id, language=lang)
    await state.update_data(lang=lang)

    await call.message.edit_text(
        t(lang, "welcome"),
        reply_markup=kb.start_onboarding_kb(lang),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "onboarding:start")
async def cb_onboarding_start(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(Onboarding.city_input)
    await call.message.edit_text(t(lang, "ask_city"))
    await call.answer()


@router.message(Onboarding.city_input)
async def handle_city_input(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    geo = await geocode_city(message.text.strip())
    if not geo:
        await message.answer(t(lang, "city_not_found"))
        return

    await state.update_data(geo=geo)
    await state.set_state(Onboarding.city_confirm)
    await message.answer(
        t(lang, "city_found", display=geo["display"]),
        reply_markup=kb.city_confirm_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "city:confirm", Onboarding.city_confirm)
async def cb_city_confirm(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    geo = data["geo"]

    tz = get_timezone(geo["lat"], geo["lon"])
    await crud.update_user(
        session,
        call.from_user.id,
        city=geo["city"],
        lat=geo["lat"],
        lon=geo["lon"],
        timezone=tz,
    )

    await state.set_state(Onboarding.skin_type)
    await call.message.edit_text(t(lang, "ask_skin"), reply_markup=kb.skin_type_kb(lang), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "city:retry", Onboarding.city_confirm)
async def cb_city_retry(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(Onboarding.city_input)
    await call.message.edit_text(t(lang, "ask_city"))
    await call.answer()


@router.callback_query(F.data.startswith("skin:"), Onboarding.skin_type)
async def cb_skin_type(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    skin = int(call.data.split(":")[1])
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await crud.update_user(session, call.from_user.id, skin_type=skin)
    await state.update_data(skin=skin)

    await state.set_state(Onboarding.exposed_area)
    await call.message.edit_text(t(lang, "ask_area"), reply_markup=kb.exposed_area_kb(lang), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data.startswith("area:"), Onboarding.exposed_area)
async def cb_exposed_area(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    area = call.data.split(":")[1]
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await crud.update_user(session, call.from_user.id, exposed_area=area)
    await state.update_data(area=area)

    await state.set_state(Onboarding.notify_hour)
    await call.message.edit_text(t(lang, "ask_hour"), reply_markup=kb.notify_hour_kb(lang), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "hour:custom", Onboarding.notify_hour)
async def cb_hour_custom(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=kb.notify_hour_custom_kb())
    await call.answer()


@router.callback_query(F.data.startswith("hour:"), Onboarding.notify_hour)
async def cb_notify_hour(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    hour = int(call.data.split(":")[1])
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await crud.update_user(session, call.from_user.id, notify_hour=hour)
    user = await crud.get_user(session, call.from_user.id)

    window_info = await _build_window_info(user, lang)

    skin_name = SKIN_NAMES[lang].get(user.skin_type, "")
    area_name = AREA_NAMES[lang].get(user.exposed_area, "")

    text = t(
        lang,
        "setup_done",
        city=user.city,
        skin=skin_name,
        area=area_name,
        hour=hour,
        window_info=window_info,
    )

    await state.clear()
    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()


async def _build_window_info(user, lang: str) -> str:
    try:
        data = await fetch_uv_data(user.lat, user.lon, user.timezone)
        window = parse_uv_window(data)
        if window:
            uv = get_peak_uv(data)
            minutes = calculate_exposure(user.skin_type or 3, user.exposed_area, uv)
            win_str = format_window(window)
            if lang == "ru":
                return f"Сегодняшнее окно УФ-B: {win_str}\nРекомендую выйти на: {minutes} мин\nUV-индекс сейчас: {uv:.0f}"
            else:
                return f"Today's UVB window: {win_str}\nRecommended: {minutes} min\nCurrent UV index: {uv:.0f}"
        else:
            if lang == "ru":
                return "Сегодня нет УФ-B окна (UV < 3)."
            else:
                return "No UVB window today (UV < 3)."
    except Exception:
        return ""
