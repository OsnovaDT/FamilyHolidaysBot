"""Main file with bot logic"""

import asyncio
from logging import INFO, basicConfig, getLogger

from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from constants.constants import ALL_MONTHS, BOT, BOT_COMMANDS, MONTHS_NUMBERS
from constants.queries import (
    ALL_HOLIDAYS_SQL_QUERY,
    NEXT_MONTH_HOLIDAYS_SQL_QUERY,
    SPECIFIED_MONTH_HOLIDAYS_SQL_QUERY,
    THIS_MONTH_HOLIDAYS_SQL_QUERY,
)
from jobs import add_daily_job, run_scheduler
from keyboards import get_months_keyboard, get_yes_no_inline_keyboard
from services import (
    add_new_daily_notification_to_db,
    change_daily_notification_time_in_db,
    delete_daily_notification_from_db,
    is_daily_notification_exists,
    send_sql_query_result_to_user,
)
from states import MonthStates, NotificationStates
from utils import (
    get_bot_commands_to_display,
    is_daily_notification_time_correct,
    send_month_choosing_instruction,
)

dp = Dispatcher()
logger = getLogger(__name__)

scheduler = AsyncIOScheduler()

BOT_COMMANDS_TO_DISPLAY = get_bot_commands_to_display(BOT_COMMANDS)


# Default commands handlers


@dp.message(CommandStart())
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


@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Handler for /help command - show all commands for the user"""

    await message.answer(BOT_COMMANDS_TO_DISPLAY)
    await send_month_choosing_instruction(message)


# Holidays commands handlers


@dp.message(Command("all_holidays"))
async def all_holidays_handler(message: Message) -> None:
    """Handler for /all_holidays command.

    Show all family's holidays and birthdays.

    """

    await send_sql_query_result_to_user(message, ALL_HOLIDAYS_SQL_QUERY)


@dp.message(Command("this_month_holidays"))
async def this_month_holidays_handler(message: Message) -> None:
    """Handler for /this_month_holidays command.

    Show family's holidays and birthdays that will be in this month.

    """

    await send_sql_query_result_to_user(message, THIS_MONTH_HOLIDAYS_SQL_QUERY)


@dp.message(Command("next_month_holidays"))
async def next_month_holidays_handler(message: Message) -> None:
    """Handler for /next_month_holidays command.

    Show family's holidays and birthdays that will be in the next month.

    """

    await send_sql_query_result_to_user(message, NEXT_MONTH_HOLIDAYS_SQL_QUERY)


# Notifications commands handlers


@dp.message(Command("add_notification"))
async def add_notification_handler(message: Message) -> None:
    """Handler for /add_notification command.

    Add daily notification about today's holiday for the user.

    """

    if await is_daily_notification_exists(message):
        await message.answer("Вы уже добавили уведомление")
    else:
        await message.answer(
            "Вы точно хотите добавить ежедневное уведомление о праздниках?",
            reply_markup=get_yes_no_inline_keyboard(
                yes_btn_name="btn_add_notification"
            ),
        )


@dp.message(Command("change_notification"))
async def change_notification_handler(
    message: Message, state: FSMContext
) -> None:
    """Handler for /change_notification command.

    Allow to change the notification's time.

    """

    if await is_daily_notification_exists(message):
        await message.answer(
            "Напишите новое время для уведомления.\nПример - <b>12:30</b>"
        )
        await state.set_state(NotificationStates.awaiting_new_time)
    else:
        await message.answer(
            "У вас не подключена отправка уведомления."
            "Вы можете подключить ее с помощью команды /add_notification",
        )


@dp.message(Command("delete_notification"))
async def delete_notification_handler(message: Message) -> None:
    """Handler for /delete_notification command.

    Delete daily notification about today's holiday for the user.

    """

    if await is_daily_notification_exists(message):
        await message.answer(
            "Вы точно хотите удалить уведомление?",
            reply_markup=get_yes_no_inline_keyboard(
                yes_btn_name="btn_delete_notification"
            ),
        )
    else:
        await message.answer("У вас нет уведомления")


# States handlers


@dp.message(MonthStates.choosing_month, F.text.in_(ALL_MONTHS))
async def specified_month_handler(message: Message):
    """Handler for choosing specified month.

    Show family's holidays and birthdays that will be in the specified month.

    """

    month = MONTHS_NUMBERS[message.text]

    await send_sql_query_result_to_user(
        message, SPECIFIED_MONTH_HOLIDAYS_SQL_QUERY.format(month=month)
    )


@dp.message(NotificationStates.awaiting_new_time)
async def daily_notification_time_handler(message: Message, state: FSMContext):
    """Handler for choosing daily notification's time.

    Change time for user's daily notification.

    """

    new_time = message.text
    chat_id = str(message.chat.id)

    if await is_daily_notification_time_correct(new_time):
        await change_daily_notification_time_in_db(BOT, new_time, chat_id)

        new_time = [int(item) for item in new_time.split(":")]

        scheduler.remove_job(chat_id)
        await add_daily_job(scheduler, chat_id, new_time)

        await state.clear()
    else:
        await message.answer("Формат некорректный")


# Buttons handlers


@dp.callback_query(F.data == "btn_add_notification")
async def process_callback_btn_add_notification(
    callback_query: CallbackQuery,
) -> None:
    """Handler for button «btn_add_notification» click.

    Add user's notification to DB and add the job.

    """

    message = callback_query.message

    await add_new_daily_notification_to_db(message)
    # TODO: Добавить возможность выбора времени
    await add_daily_job(scheduler, str(message.chat.id), [9, 0])


@dp.callback_query(F.data == "btn_delete_notification")
async def process_callback_btn_delete_notification(
    callback_query: CallbackQuery,
) -> None:
    """Handler for button «btn_delete_notification» click.

    Delete user's notification from DB and delete the job.

    """

    message = callback_query.message

    await delete_daily_notification_from_db(message)
    scheduler.remove_job(str(message.chat.id))


async def main() -> None:
    """Main function that runs the bot"""

    try:
        asyncio.create_task(run_scheduler(scheduler))
        await BOT.set_my_commands(BOT_COMMANDS)
        await dp.start_polling(BOT)
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
    asyncio.run(main())
