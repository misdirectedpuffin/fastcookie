import logging
import os
import asyncio

from sqlalchemy import text
from tenacity import retry
from tenacity.after import after_log
from tenacity.before import before_log
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from config import settings
from db.session import SyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    if settings.ENV == 'test':
        logger.info("[TEST] Skipping post start scripts.")
        return
    logger.info("Running post start scripts...")
    logger.info("Nothing to do.")



if __name__ == "__main__":
    init()
