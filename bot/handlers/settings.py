from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot import keyboards as kb
from bot.messages import t
from core.uv import geocode_city, get_timezone
from db import crud

router = Router()


class SettingsFSM(StatesGroup):
    city_input = State()
    city_confirm = State()
    skin_type = State()
    exposed_area = State()
    notify_hour = State()
    language = State()


@router.message(Command("settings"))
async def cmd_settings(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    user = await crud.get_user(session, message.from_user.id)
    lang = user.language if user else "ru"
    await message.answer(t(lang, "settings_menu"), reply_markup=kb.settings_kb(lang), parse_mode="HTML")


@router.callback_query(F.data == "settings:city")
async def settings_city(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    lang = user.language if user else "ru"
    await state.set_state(SettingsFSM.city_input)
    await state.update_data(lang=lang)
    await call.message.answer(t(lang, "ask_city"))
    await call.answer()


@router.callback_query(F.data == "settings:skin")
async def settings_skin(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    lang = user.language if user else "ru"
    await state.set_state(SettingsFSM.skin_type)
    await state.update_data(lang=lang)
    await call.message.answer(t(lang, "ask_skin"), reply_markup=kb.skin_type_kb(lang), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "settings:area")
async def settings_area(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    lang = user.language if user else "ru"
    await state.set_state(SettingsFSM.exposed_area)
    await state.update_data(lang=lang)
    await call.message.answer(t(lang, "ask_area"), reply_markup=kb.exposed_area_kb(lang), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "settings:hour")
async def settings_hour(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    lang = user.language if user else "ru"
    await state.set_state(SettingsFSM.notify_hour)
    await state.update_data(lang=lang)
    await call.message.answer(t(lang, "ask_hour"), reply_markup=kb.notify_hour_kb(lang), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "settings:lang")
async def settings_lang(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    lang = user.language if user else "ru"
    await state.set_state(SettingsFSM.language)
    await state.update_data(lang=lang)
    await call.message.answer(t(lang, "choose_language"), reply_markup=kb.language_kb())
    await call.answer()


@router.callback_query(F.data == "settings:evening")
async def settings_evening(call: CallbackQuery, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    if not user:
        await call.answer()
        return
    lang = user.language
    new_val = not user.evening_notify
    await crud.update_user(session, call.from_user.id, evening_notify=new_val)
    key = "evening_notify_on" if new_val else "evening_notify_off"
    await call.message.answer(t(lang, key))
    await call.answer()


@router.callback_query(F.data == "settings:leaderboard")
async def settings_leaderboard(call: CallbackQuery, session: AsyncSession):
    user = await crud.get_user(session, call.from_user.id)
    if not user:
        await call.answer()
        return
    lang = user.language
    new_val = not user.leaderboard_opt_in
    await crud.update_user(session, call.from_user.id, leaderboard_opt_in=new_val)
    key = "leaderboard_on" if new_val else "leaderboard_off"
    await call.message.answer(t(lang, key))
    await call.answer()


@router.message(SettingsFSM.city_input)
async def settings_city_input(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    geo = await geocode_city(message.text.strip())
    if not geo:
        await message.answer(t(lang, "city_not_found"))
        return
    await state.update_data(geo=geo)
    await state.set_state(SettingsFSM.city_confirm)
    await message.answer(t(lang, "city_found", display=geo["display"]), reply_markup=kb.city_confirm_kb(lang), parse_mode="HTML")


@router.callback_query(F.data == "city:confirm", SettingsFSM.city_confirm)
async def settings_city_confirm(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    geo = data["geo"]
    tz = get_timezone(geo["lat"], geo["lon"])
    await crud.update_user(session, call.from_user.id, city=geo["city"], lat=geo["lat"], lon=geo["lon"], timezone=tz)
    await state.clear()
    await call.message.edit_text(t(lang, "city_updated", display=geo["display"]), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "city:retry", SettingsFSM.city_confirm)
async def settings_city_retry(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(SettingsFSM.city_input)
    await call.message.edit_text(t(lang, "ask_city"))
    await call.answer()


@router.callback_query(F.data.startswith("skin:"), SettingsFSM.skin_type)
async def settings_skin_select(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    skin = int(call.data.split(":")[1])
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await crud.update_user(session, call.from_user.id, skin_type=skin)
    await state.clear()
    await call.message.edit_text(t(lang, "skin_updated"))
    await call.answer()


@router.callback_query(F.data.startswith("area:"), SettingsFSM.exposed_area)
async def settings_area_select(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    area = call.data.split(":")[1]
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await crud.update_user(session, call.from_user.id, exposed_area=area)
    await state.clear()
    await call.message.edit_text(t(lang, "area_updated"))
    await call.answer()


@router.callback_query(F.data.startswith("hour:"), SettingsFSM.notify_hour)
async def settings_hour_select(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    hour = int(call.data.split(":")[1])
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await crud.update_user(session, call.from_user.id, notify_hour=hour)
    await state.clear()
    await call.message.edit_text(t(lang, "hour_updated", hour=hour))
    await call.answer()


@router.callback_query(F.data == "hour:custom", SettingsFSM.notify_hour)
async def settings_hour_custom(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=kb.notify_hour_custom_kb())
    await call.answer()


@router.callback_query(F.data.startswith("lang:"), SettingsFSM.language)
async def settings_lang_select(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    lang = call.data.split(":")[1]
    await crud.update_user(session, call.from_user.id, language=lang)
    await state.clear()
    await call.message.edit_text(t(lang, "lang_updated"))
    await call.answer()
