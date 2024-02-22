"""Main file with bot logic"""

from asyncio import run
from logging import INFO, basicConfig, getLogger

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from constants import (
    ALL_HOLIDAYS_SQL_QUERY,
    ALL_MONTHS,
    BOT_COMMANDS,
    MONTHS_NUMBERS,
    NEXT_MONTH_HOLIDAYS_SQL_QUERY,
    SPECIFIED_MONTH_HOLIDAYS_SQL_QUERY,
    THIS_MONTH_HOLIDAYS_SQL_QUERY,
    TOKEN,
)
from services import (
    get_months_keyboard,
    send_month_choosing_instruction,
    send_sql_query_result_to_user,
)
from states import MonthStates
from utils import get_bot_commands_to_display

dispatcher = Dispatcher()

logger = getLogger(__name__)


BOT_COMMANDS_TO_DISPLAY = get_bot_commands_to_display(BOT_COMMANDS)


@dispatcher.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    """Handler for /start command - greets the user"""

    await state.set_state(MonthStates.choosing_month)

    greeting_text = (
        f"Привет, {message.from_user.full_name}!\n\n"
        "Я помогу тебе не забыть о важных праздниках твоей семьи! 👨‍👩‍👧‍👦\n\n"
        "Вот команды, которые ты можешь использовать:\n"
    ) + BOT_COMMANDS_TO_DISPLAY

    await message.answer_photo(
        FSInputFile("photos/cat.jpg"),
        greeting_text,
        reply_markup=get_months_keyboard(),
    )
    await send_month_choosing_instruction(message)


@dispatcher.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Handler for /help command - show all commands for the user"""

    await message.answer(BOT_COMMANDS_TO_DISPLAY)
    await send_month_choosing_instruction(message)


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


@dispatcher.message(MonthStates.choosing_month, F.text.in_(ALL_MONTHS))
async def specified_month_handler(message: Message):
    """Handler for choosing specified month.

    Show family's holidays and birthdays that will be in the specified month.

    """

    month = MONTHS_NUMBERS[message.text]

    await send_sql_query_result_to_user(
        message, SPECIFIED_MONTH_HOLIDAYS_SQL_QUERY.format(month=month)
    )


async def main() -> None:
    """Main function that runs the bot"""

    try:
        bot = Bot(
            TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

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
