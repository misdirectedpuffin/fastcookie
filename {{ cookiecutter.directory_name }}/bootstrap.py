import logging
import asyncio

from fastapi.applications import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware.cors import CORSMiddleware

from config import Settings
from api.{{cookiecutter.first_module_name}}.models import DbModel
from api.router import api_router

logger = logging.getLogger()


class BootstrapApp:
    def __init__(self, app: FastAPI, settings: Settings) -> None:
        self.app = app
        self.settings = settings

    def create_app(self):
        if self.settings.API.CORS_ORIGINS:
            logger.debug("Added backend CORS Origins %s", self.settings.API.CORS_ORIGINS)
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.settings.API.CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        logger.info("Include router")
        self.app.include_router(api_router, prefix=self.settings.API.V1_STR)


class BootstrapDatabase:
    def __init__(self, settings: Settings, engine: AsyncEngine) -> None:
        self.settings = settings
        self.engine = engine
        self.metadata = DbModel.metadata

    async def create_all(self) -> None:
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(self.metadata.drop_all)
            async with self.engine.begin() as conn:
                await conn.run_sync(self.metadata.create_all)
        except AttributeError:
            logger.exception("Failed to create all tables.")
        else:
            logger.info("Created tables!!")

    async def drop_all(self) -> None:
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(self.metadata.drop_all)
        except AttributeError:
            logger.exception("Failed to drop all tables.")
        else:
            logger.info("Dropped tables!!")

    async def init_database(self):
        async def create_defaults():
            logger.info("No tasks have been created. Sleeping.")
            await asyncio.sleep(1)

        await asyncio.create_task(create_defaults())
