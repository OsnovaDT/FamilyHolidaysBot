"""Utils of the project"""

from datetime import date
from math import ceil
from typing import List

from custom_types import TypeHoliday

# TODO: async


async def get_formatted_holidays(holidays: List[TypeHoliday]) -> str:
    """Return holidays in necessary format"""

    formatted_holidays = ""

    if not isinstance(holidays, list):
        return formatted_holidays

    for holiday in holidays:
        formatted_holidays += await _get_formatted_single_holiday(holiday)

    return formatted_holidays


async def _get_formatted_single_holiday(holiday: TypeHoliday) -> str:
    """Format holiday text and return"""

    if not isinstance(holiday, tuple):
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


async def _get_days_left(holiday_date: date) -> int | None:
    """Return how many days left until the holiday"""

    if not isinstance(holiday_date, date):
        # TODO: Add log
        return None

    # TODO: Учесть прошедшие даты
    nearest_holiday_date = holiday_date.replace(year=date.today().year)

    return (nearest_holiday_date - date.today()).days


async def _get_age_suffix(age: int | str) -> str:
    """Return suffix for the age.

    For example:
    >>> get_age_suffix(14) = лет
    >>> get_age_suffix(21) = год
    >>> get_age_suffix(42) = года
    >>> get_age_suffix(55) = лет

    """

    suffix = ""
    age = str(age)

    if not isinstance(age, (int, str)):
        return suffix

    first_digit, last_digit = age[0], age[-1]

    if first_digit != "1":
        if last_digit == "1":
            suffix = "год"
        elif last_digit in ("2", "3", "4"):
            suffix = "года"

    return suffix or "лет"
