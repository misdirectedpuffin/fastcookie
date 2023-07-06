import logging

from sqlalchemy import text
from tenacity import retry
from tenacity.after import after_log
from tenacity.before import before_log
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed
import asyncio
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
    try:
        logger.info("Initializing service")
        # Try to create session to check if database is awake
        with SyncSessionLocal() as session:
            session.execute(text("SELECT 1"))
    except Exception as exc:
        logger.info("[Prestart] Unable to connect to db.")
        # await database.rollback()
        logger.error(exc)
        raise exc
    else:
        logger.info("[Prestart] Session success.")


if __name__ == "__main__":
    init()
