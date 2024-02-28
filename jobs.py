"""Scheduler's jobs"""

from asyncio import CancelledError, sleep
from logging import getLogger
from typing import Tuple

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from constants.constants import BOT
from services import get_daily_notifications_from_db, send_today_holidays

logger = getLogger(__name__)


async def add_daily_job(
    scheduler: AsyncIOScheduler, chat_id: str, time_: Tuple[int, int]
) -> None:
    """Add daily job for scheduler"""

    chat_id = str(chat_id)
    hour, minute = time_

    scheduler.add_job(
        send_today_holidays,
        "cron",
        args=[BOT, chat_id],
        hour=hour,
        minute=minute,
        id=chat_id,
    )


async def run_scheduler(scheduler) -> None:
    """Run scheduler with jobs"""

    daily_notifications = await get_daily_notifications_from_db()

    if daily_notifications:
        for chat_id, time_ in daily_notifications.items():
            await add_daily_job(scheduler, chat_id, time_)

    scheduler.start()

    try:
        while True:
            await sleep(60)
    except (CancelledError, KeyboardInterrupt):
        logger.info("Scheduler stopped")
        scheduler.shutdown()
