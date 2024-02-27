"""Utils of the project"""

from datetime import date
from logging import getLogger
from math import ceil
from typing import Dict, List

from aiogram.types import FSInputFile, Message

from constants.constants import ERROR_MESSAGE
from custom_types import TypeHoliday

logger = getLogger(__name__)


async def get_formatted_holidays(
    holidays: List[TypeHoliday], is_notification=False
) -> str:
    """Return holidays in necessary format"""

    formatted_holidays = ""

    if not isinstance(holidays, list):
        logger.error(
            "Wrong «holidays» type - %hd («get_formatted_holidays» func)",
            holidays,
        )
        return ERROR_MESSAGE

    if is_notification:
        formatted_holidays = "Привет! 👋"

        for holiday in holidays:
            formatted_holidays += "\n\n" + (
                await _get_formatted_single_holiday_for_notification(holiday)
            )
    else:
        for holiday in holidays:
            formatted_holidays += await _get_formatted_single_holiday(holiday)

    return formatted_holidays


async def _get_formatted_single_holiday(holiday: TypeHoliday) -> str:
    """Format holiday text and return"""

    if not isinstance(holiday, tuple):
        logger.error(
            "Wrong «holiday» type - %hd "
            "(«_get_formatted_single_holiday» func)",
            holiday,
        )
        return ""

    holiday_date, title, is_birthday, whom_to_congratulate = holiday

    days_left = await _get_days_left(holiday_date)

    text = f'<b>{title} - {holiday_date.strftime("%d %B")}</b>\n'
    text += f"⏳ <u>Осталось дней:</u> {days_left}\n"

    if is_birthday:
        # TODO: FIX
        age = ceil((date.today() - holiday_date).days / 365)
        age_suffix = await _get_age_suffix(age)

        text += f"🗓️ <u>Сколько исполнится:</u> {age} {age_suffix}"
    else:
        text += f"🎉 <u>Кого поздравляем:</u> {whom_to_congratulate}"

    return text + "\n\n"


async def _get_formatted_single_holiday_for_notification(
    holiday: TypeHoliday,
) -> str:
    """Format holiday text and return"""

    if not isinstance(holiday, tuple):
        logger.error(
            "Wrong «holiday» type - %hd "
            "(«_get_formatted_single_holiday» func)",
            holiday,
        )
        return ""

    holiday_date, title, is_birthday, whom_to_congratulate = holiday

    if is_birthday:
        age = _get_person_age(holiday_date)
        age_suffix = await _get_age_suffix(age)

        text = f"Сегодня <b>{title}</b>.\n"
        text += f"Исполнилось <b>{age} {age_suffix}</b>\n"
        text += "Не забудь поздравить! 🎉"
    else:
        text = f"Сегодня праздник - <b>{title}</b>\n"
        text += f"Не забудь поздравить причастных 🎉: {whom_to_congratulate}"

    return text


async def _get_days_left(holiday_date: date) -> int | str:
    """Return how many days left until the holiday"""

    if not isinstance(holiday_date, date):
        logger.error(
            "Wrong «holiday_date» type - %hd («_get_days_left» func)",
            holiday_date,
        )
        return "Не удалось вычислить"

    # TODO: Учесть прошедшие даты
    nearest_holiday_date = holiday_date.replace(year=date.today().year)

    return (nearest_holiday_date - date.today()).days


async def _get_age_suffix(age: int | str) -> str:
    """Return suffix for the age.

    >>> get_age_suffix(-1) = ''
    >>> get_age_suffix(14) = 'лет'
    >>> get_age_suffix(21) = 'год'
    >>> get_age_suffix(42) = 'года'

    """

    suffix = "лет"

    if not isinstance(age, (int, str)) or int(age) <= 0:
        return ""

    age = str(age)

    if not (age.startswith("1") and len(age) == 2):
        last_digit = age[-1]

        if last_digit == "1":
            suffix = "год"
        elif last_digit in ("2", "3", "4"):
            suffix = "года"

    return suffix


def get_bot_commands_to_display(bot_commands: List[Dict[str, str]]) -> str:
    """Return bot's commands in text to display to the user"""

    return "\n".join(
        [
            f"/{command['command']} - {command['description']}"
            for command in bot_commands
        ]
    )


async def send_month_choosing_instruction(message: Message) -> None:
    """Send instruction about month choosing"""

    await message.answer_photo(
        FSInputFile("photos/month_choosing_button.png"),
        "Также ты можешь получить <u>праздники в конкретном месяце</u>."
        " Для этого нажми на эту кнопку 👆",
    )


async def _get_person_age(birthday: date) -> int:
    """Return age for person by birthday"""

    # TODO: Fix
    return ceil((date.today() - birthday).days / 365)
