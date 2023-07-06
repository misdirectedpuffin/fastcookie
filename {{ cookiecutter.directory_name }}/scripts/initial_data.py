import logging
import asyncio
from os import getenv


from bootstrap import BootstrapDatabase
from config import settings, Settings
from db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(config: Settings, session) -> None:
    try:
        env = getenv("ENV") or "development"
        if env == "test":
            logger.info("[TEST] Skipping db bootstrap.")
            return
        else:
            db = BootstrapDatabase(config, session)
            await db.init_database()
    except Exception:
        logger.exception("[Initial Data] Something went wrong.")
    else:
        logger.info("[Initial data] Success!")


if __name__ == "__main__":

    asyncio.run(main(settings, SessionLocal()))
