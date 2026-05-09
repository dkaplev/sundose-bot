from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def language_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
    )
    return builder.as_markup()


def start_onboarding_kb(lang: str) -> InlineKeyboardMarkup:
    label = "Поехали! 🚀" if lang == "ru" else "Let's go! 🚀"
    builder = InlineKeyboardBuilder()
    builder.button(text=label, callback_data="onboarding:start")
    return builder.as_markup()


def city_confirm_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    correct = "✅ Верно" if lang == "ru" else "✅ Correct"
    fix = "✏️ Исправить" if lang == "ru" else "✏️ Fix"
    builder.row(
        InlineKeyboardButton(text=correct, callback_data="city:confirm"),
        InlineKeyboardButton(text=fix, callback_data="city:retry"),
    )
    return builder.as_markup()


def skin_type_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if lang == "ru":
        skins = [
            ("🏻 Очень светлая — всегда обгораю", "skin:1"),
            ("🏼 Светлая — иногда обгораю", "skin:2"),
            ("🏽 Средняя — редко обгораю", "skin:3"),
            ("🏾 Смуглая — почти не обгораю", "skin:4"),
            ("🏿 Тёмная — никогда не обгораю", "skin:5"),
        ]
    else:
        skins = [
            ("🏻 Very light — always burn", "skin:1"),
            ("🏼 Light — sometimes burn", "skin:2"),
            ("🏽 Medium — rarely burn", "skin:3"),
            ("🏾 Tan — almost never burn", "skin:4"),
            ("🏿 Dark — never burn", "skin:5"),
        ]
    for text, data in skins:
        builder.button(text=text, callback_data=data)
    builder.adjust(1)
    return builder.as_markup()


def exposed_area_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if lang == "ru":
        areas = [
            ("💪 Только руки и лицо", "area:arms"),
            ("🦵 Руки + ноги (шорты/платье)", "area:arms_legs"),
            ("🏊 Руки + ноги + живот (пляж)", "area:full"),
        ]
    else:
        areas = [
            ("💪 Arms and face only", "area:arms"),
            ("🦵 Arms + legs (shorts/dress)", "area:arms_legs"),
            ("🏊 Arms + legs + torso (beach)", "area:full"),
        ]
    for text, data in areas:
        builder.button(text=text, callback_data=data)
    builder.adjust(1)
    return builder.as_markup()


def notify_hour_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for h in [7, 8, 9, 10, 11]:
        builder.button(text=f"{h}:00", callback_data=f"hour:{h}")
    label = "Другое время..." if lang == "ru" else "Other time..."
    builder.button(text=label, callback_data="hour:custom")
    builder.adjust(3)
    return builder.as_markup()


def notify_hour_custom_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for h in range(6, 13):
        builder.button(text=f"{h}:00", callback_data=f"hour:{h}")
    builder.adjust(4)
    return builder.as_markup()


def morning_notification_kb(lang: str, date_str: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if lang == "ru":
        builder.row(
            InlineKeyboardButton(text="✅ Вышел сегодня", callback_data=f"went_out:{date_str}"),
            InlineKeyboardButton(text="⏭ Пропустил", callback_data=f"skipped:{date_str}"),
        )
        builder.row(
            InlineKeyboardButton(text="📍 Сменить город", callback_data="settings:city")
        )
    else:
        builder.row(
            InlineKeyboardButton(text="✅ Went out", callback_data=f"went_out:{date_str}"),
            InlineKeyboardButton(text="⏭ Skipped", callback_data=f"skipped:{date_str}"),
        )
        builder.row(
            InlineKeyboardButton(text="📍 Change city", callback_data="settings:city")
        )
    return builder.as_markup()


def settings_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if lang == "ru":
        items = [
            ("📍 Изменить город", "settings:city"),
            ("🎨 Тип кожи", "settings:skin"),
            ("👕 Открытая зона", "settings:area"),
            ("🔔 Время уведомлений", "settings:hour"),
            ("🌍 Язык / Language", "settings:lang"),
        ]
    else:
        items = [
            ("📍 Change city", "settings:city"),
            ("🎨 Skin type", "settings:skin"),
            ("👕 Exposed area", "settings:area"),
            ("🔔 Notification time", "settings:hour"),
            ("🌍 Language / Язык", "settings:lang"),
        ]
    for text, data in items:
        builder.button(text=text, callback_data=data)
    builder.adjust(1)
    return builder.as_markup()
