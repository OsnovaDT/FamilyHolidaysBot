"""All business-logic of the project"""

from logging import getLogger

from aiogram.types import FSInputFile, Message
from mysql.connector import Error

from constants.constants import DB_CONNECT, ERROR_MESSAGE
from constants.queries import (
    ADD_DAILY_NOTIFICATIONS_QUERY,
    DELETE_DAILY_NOTIFICATIONS_QUERY,
    GET_DAILY_NOTIFICATIONS_CHATS_IDS_QUERY,
    IS_EXISTS_DAILY_NOTIFICATIONS_QUERY,
    TODAYS_HOLIDAYS_SQL_QUERY,
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


async def is_daily_notification_exists(message: Message) -> bool:
    """Check is there is the user's daily notification"""

    try:
        cursor.execute(
            IS_EXISTS_DAILY_NOTIFICATIONS_QUERY.format(chat_id=message.chat.id)
        )

        return bool(cursor.fetchone()[0])
    except Error as error:
        logger.error(error)
        await message.answer_photo(
            FSInputFile("photos/tinkoff.jpg"),
            ERROR_MESSAGE,
        )


async def get_daily_notifications_chats_ids() -> None:
    """Return all chat ids for daily notifications"""

    try:
        cursor.execute(GET_DAILY_NOTIFICATIONS_CHATS_IDS_QUERY)

        return tuple(chat_id[0] for chat_id in cursor.fetchall())
    except Error as error:
        logger.error(error)


async def add_new_daily_notification_to_db(message: Message) -> None:
    """Add a new daily notification for the user"""

    try:
        cursor.execute(
            ADD_DAILY_NOTIFICATIONS_QUERY.format(chat_id=message.chat.id)
        )
        DB_CONNECT.commit()

        await message.answer("Уведомление добавлено! ☑️")
    except Error as error:
        logger.error(error)
        await message.answer_photo(
            FSInputFile("photos/tinkoff.jpg"),
            ERROR_MESSAGE,
        )


async def delete_daily_notification_from_db(message: Message) -> None:
    """Delete daily notification for the user"""

    try:
        cursor.execute(
            DELETE_DAILY_NOTIFICATIONS_QUERY.format(chat_id=message.chat.id)
        )
        DB_CONNECT.commit()

        await message.answer("Уведомление отключено! ☑️")
    except Error as error:
        logger.error(error)
        await message.answer_photo(
            FSInputFile("photos/tinkoff.jpg"),
            ERROR_MESSAGE,
        )


async def send_today_holidays(bot, chat_id: str) -> None:
    """Send today's holidays to the user"""

    try:
        cursor.execute(TODAYS_HOLIDAYS_SQL_QUERY)
        holidays = cursor.fetchall()

        if holidays:
            holidays_info = await get_formatted_holidays(holidays, True)
            await bot.send_message(chat_id=chat_id, text=holidays_info)
    except Error as error:
        logger.error(error)
        await bot.answer_photo(
            FSInputFile("photos/tinkoff.jpg"),
            ERROR_MESSAGE,
        )
