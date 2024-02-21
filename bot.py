"""Main file with bot logic"""

from asyncio import run
from logging import INFO, basicConfig
from sys import stdout

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from mysql.connector import Error

from constants import ALL_HOLIDAYS_SQL_QUERY, BOT_COMMANDS, DB_CONNECT, TOKEN
from utils import get_formatted_holidays

dispatcher = Dispatcher()

cursor = DB_CONNECT.cursor()


@dispatcher.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handler for /start command.

    Greets the user.

    """

    # TODO: Add links
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n\n"
        "Вот команды, которые ты можешь использовать:\n"
        "\\start\n"
        "\\help\n"
        "\\all_holidays"
    )


@dispatcher.message(Command("all_holidays"))
async def command_all_holidays_handler(message: Message) -> None:
    """Handler for /all_holidays command.

    Show all family's holidays and birthdays.

    """

    try:
        cursor.execute(ALL_HOLIDAYS_SQL_QUERY)
        all_holidays = await get_formatted_holidays(cursor.fetchall())

        await message.answer(all_holidays)
    except Error as e:
        # TODO: Add logs
        print(e)


async def main() -> None:
    """Main function that runs the bot"""

    # TODO: Add logs
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await bot.set_my_commands(BOT_COMMANDS)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    basicConfig(level=INFO, stream=stdout)
    run(main())
