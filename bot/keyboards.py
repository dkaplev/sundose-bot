from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def language_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
    )
    return builder.as_markup()


def start_onboarding_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Поехали! 🚀" if lang == "ru" else "Let's go! 🚀", callback_data="onboarding:start")
    return builder.as_markup()


def city_confirm_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Верно" if lang == "ru" else "✅ Correct", callback_data="city:confirm"),
        InlineKeyboardButton(text="✏️ Исправить" if lang == "ru" else "✏️ Fix", callback_data="city:retry"),
    )
    return builder.as_markup()


def skin_type_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    skins = (
        [
            ("🏻 Очень светлая — всегда обгораю", "skin:1"),
            ("🏼 Светлая — иногда обгораю", "skin:2"),
            ("🏽 Средняя — редко обгораю", "skin:3"),
            ("🏾 Смуглая — почти не обгораю", "skin:4"),
            ("🏿 Тёмная — никогда не обгораю", "skin:5"),
        ] if lang == "ru" else [
            ("🏻 Very light — always burn", "skin:1"),
            ("🏼 Light — sometimes burn", "skin:2"),
            ("🏽 Medium — rarely burn", "skin:3"),
            ("🏾 Tan — almost never burn", "skin:4"),
            ("🏿 Dark — never burn", "skin:5"),
        ]
    )
    for text, data in skins:
        builder.button(text=text, callback_data=data)
    builder.adjust(1)
    return builder.as_markup()


def exposed_area_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    areas = (
        [
            ("💪 Только руки и лицо", "area:arms"),
            ("🦵 Руки + ноги (шорты/платье)", "area:arms_legs"),
            ("🏊 Руки + ноги + живот (пляж)", "area:full"),
        ] if lang == "ru" else [
            ("💪 Arms and face only", "area:arms"),
            ("🦵 Arms + legs (shorts/dress)", "area:arms_legs"),
            ("🏊 Arms + legs + torso (beach)", "area:full"),
        ]
    )
    for text, data in areas:
        builder.button(text=text, callback_data=data)
    builder.adjust(1)
    return builder.as_markup()


def notify_hour_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for h in [7, 8, 9, 10, 11]:
        builder.button(text=f"{h}:00", callback_data=f"hour:{h}")
    builder.button(text="Другое время..." if lang == "ru" else "Other time...", callback_data="hour:custom")
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
        builder.row(InlineKeyboardButton(text="📍 Сменить город", callback_data="settings:city"))
    else:
        builder.row(
            InlineKeyboardButton(text="✅ Went out", callback_data=f"went_out:{date_str}"),
            InlineKeyboardButton(text="⏭ Skipped", callback_data=f"skipped:{date_str}"),
        )
        builder.row(InlineKeyboardButton(text="📍 Change city", callback_data="settings:city"))
    return builder.as_markup()


def now_active_kb(lang: str, date_str: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if lang == "ru":
        builder.row(
            InlineKeyboardButton(text="✅ Вышел", callback_data=f"went_out:{date_str}"),
            InlineKeyboardButton(text="⏰ Напомни через 30 мин", callback_data="remind:30"),
        )
    else:
        builder.row(
            InlineKeyboardButton(text="✅ Went out", callback_data=f"went_out:{date_str}"),
            InlineKeyboardButton(text="⏰ Remind in 30 min", callback_data="remind:30"),
        )
    return builder.as_markup()


def now_inactive_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    label = "🔔 Напомни за 30 мин" if lang == "ru" else "🔔 Remind 30 min before"
    builder.button(text=label, callback_data="remind:window")
    return builder.as_markup()


def alone_or_together_kb(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if lang == "ru":
        builder.row(
            InlineKeyboardButton(text="🙋 Один", callback_data="session:alone"),
            InlineKeyboardButton(text="👫 С кем-то", callback_data="session:together"),
        )
    else:
        builder.row(
            InlineKeyboardButton(text="🙋 Alone", callback_data="session:alone"),
            InlineKeyboardButton(text="👫 With someone", callback_data="session:together"),
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
            ("🌙 Вечерний прогноз", "settings:evening"),
            ("🏙 Рейтинг городов", "settings:leaderboard"),
            ("🌍 Язык / Language", "settings:lang"),
        ]
    else:
        items = [
            ("📍 Change city", "settings:city"),
            ("🎨 Skin type", "settings:skin"),
            ("👕 Exposed area", "settings:area"),
            ("🔔 Notification time", "settings:hour"),
            ("🌙 Evening forecast", "settings:evening"),
            ("🏙 City leaderboard", "settings:leaderboard"),
            ("🌍 Language / Язык", "settings:lang"),
        ]
    for text, data in items:
        builder.button(text=text, callback_data=data)
    builder.adjust(1)
    return builder.as_markup()


def main_reply_kb(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    label = "☀️ Проверить сейчас" if lang == "ru" else "☀️ Check now"
    builder.button(text=label)
    return builder.as_markup(resize_keyboard=True)
