"""Scheduler's jobs"""

import asyncio
from logging import getLogger

from constants.constants import BOT
from services import get_daily_notifications_chats_ids, send_today_holidays

logger = getLogger(__name__)


async def add_daily_job(scheduler, chat_id: str) -> None:
    """Add daily job for scheduler"""

    chat_id = str(chat_id)

    scheduler.add_job(
        send_today_holidays,
        "cron",
        args=[BOT, chat_id],
        hour=9,
        minute=0,
        id=chat_id,
    )


async def run_scheduler(scheduler) -> None:
    """Run scheduler with jobs"""

    chats_ids = await get_daily_notifications_chats_ids()

    if chats_ids:
        for chat_id in chats_ids:
            await add_daily_job(scheduler, chat_id)

    scheduler.start()

    try:
        while True:
            await asyncio.sleep(60)
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Scheduler stopped")
        scheduler.shutdown()
