"""All keyboards"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from constants.constants import (
    AUTUMN_MONTHS,
    SPRING_MONTHS,
    SUMMER_MONTHS,
    WINTER_MONTHS,
)


def get_months_keyboard() -> ReplyKeyboardMarkup:
    """Return keyboard with months"""

    keyboard = [
        [KeyboardButton(text=item) for item in WINTER_MONTHS],
        [KeyboardButton(text=item) for item in SPRING_MONTHS],
        [KeyboardButton(text=item) for item in SUMMER_MONTHS],
        [KeyboardButton(text=item) for item in AUTUMN_MONTHS],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_yes_no_inline_keyboard(
    yes_btn_name: str, no_btn_name: str = "btn_no"
) -> InlineKeyboardMarkup:
    """Return inline keyboard with «Yes» and «No» buttons"""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да ✅", callback_data=yes_btn_name),
                InlineKeyboardButton(text="Нет ❌", callback_data=no_btn_name),
            ]
        ]
    )
