"""All business-logic of the project"""

from logging import getLogger

from aiogram.types import FSInputFile, Message
from mysql.connector import Error

from constants import DB_CONNECT, ERROR_MESSAGE
from utils import get_formatted_holidays

cursor = DB_CONNECT.cursor()

logger = getLogger(__name__)


async def send_sql_query_result_to_user(
    message: Message, sql_query: str
) -> None:
    """Execute SQL query, format the result and send to the user"""

    try:
        cursor.execute(sql_query)
        holidays = await get_formatted_holidays(cursor.fetchall())

        await message.answer(holidays)
    except Error as error:
        logger.error(error)
        await message.answer_photo(
            FSInputFile("photos/tinkoff.jpg"),
            ERROR_MESSAGE,
        )
