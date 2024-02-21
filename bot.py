"""Main file with bot logic"""

from asyncio import run
from logging import INFO, basicConfig, getLogger

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from constants import (
    ALL_HOLIDAYS_SQL_QUERY,
    BOT_COMMANDS,
    NEXT_MONTH_HOLIDAYS_SQL_QUERY,
    THIS_MONTH_HOLIDAYS_SQL_QUERY,
    TOKEN,
)
from services import send_sql_query_result_to_user
from utils import get_bot_commands_to_display

dispatcher = Dispatcher()

logger = getLogger(__name__)


@dispatcher.message(CommandStart())
async def start_handler(message: Message) -> None:
    """Handler for /start command - greets the user"""

    commands = get_bot_commands_to_display(BOT_COMMANDS)
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n\n"
        f"Вот команды, которые ты можешь использовать:\n{commands}"
    )


@dispatcher.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Handler for /help command - show all commands for the user"""

    commands = get_bot_commands_to_display(BOT_COMMANDS[1:])
    await message.answer(commands)


@dispatcher.message(Command("all_holidays"))
async def all_holidays_handler(message: Message) -> None:
    """Handler for /all_holidays command.

    Show all family's holidays and birthdays.

    """

    await send_sql_query_result_to_user(message, ALL_HOLIDAYS_SQL_QUERY)


@dispatcher.message(Command("this_month_holidays"))
async def this_month_holidays_handler(message: Message) -> None:
    """Handler for /this_month_holidays command.

    Show family's holidays and birthdays that will be in this month.

    """

    await send_sql_query_result_to_user(message, THIS_MONTH_HOLIDAYS_SQL_QUERY)


@dispatcher.message(Command("next_month_holidays"))
async def next_month_holidays_handler(message: Message) -> None:
    """Handler for /next_month_holidays command.

    Show family's holidays and birthdays that will be in the next month.

    """

    await send_sql_query_result_to_user(message, NEXT_MONTH_HOLIDAYS_SQL_QUERY)


async def main() -> None:
    """Main function that runs the bot"""

    try:
        bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
        await bot.set_my_commands(BOT_COMMANDS)
        await dispatcher.start_polling(bot)
    except Exception as error:
        logger.error(error)


if __name__ == "__main__":
    # TODO: в .ini, разные уровни логирования
    basicConfig(
        level=INFO,
        filename="logs.log",
        filemode="a",
        format=(
            "\n%(asctime)s.%(msecs)d - %(levelname)s (%(name)s)\n%(message)s"
        ),
        datefmt="%F %T",
    )
    run(main())
