"""All business-logic of the project"""

from logging import getLogger

from aiogram.types import (
    FSInputFile,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from mysql.connector import Error

from constants import (
    AUTUMN_MONTHS,
    DB_CONNECT,
    ERROR_MESSAGE,
    SPRING_MONTHS,
    SUMMER_MONTHS,
    WINTER_MONTHS,
)
from utils import get_formatted_holidays

cursor = DB_CONNECT.cursor()

logger = getLogger(__name__)


async def send_sql_query_result_to_user(
    message: Message, sql_query: str
) -> None:
    """Execute SQL query, format the result and send to the user"""

    try:
        cursor.execute(sql_query)
        holidays = cursor.fetchall()

        if holidays:
            holidays_info = await get_formatted_holidays(holidays)
        else:
            holidays_info = "Праздников в этот период нет"

        await message.answer(holidays_info)
    except Error as error:
        logger.error(error)
        await message.answer_photo(
            FSInputFile("photos/tinkoff.jpg"),
            ERROR_MESSAGE,
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


async def send_month_choosing_instruction(message: Message) -> None:
    """Send instruction about month choosing"""

    await message.answer_photo(
        FSInputFile("photos/month_choosing_button.png"),
        "Также ты можешь получить <u>праздники в конкретном месяце</u>."
        " Для этого нажми на эту кнопку 👆",
    )
