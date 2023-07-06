from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True  # , connect_args={"options": "-csearch_path=public"}
)
sync_engine = create_engine(settings.SQLALCHEMY_SYNC_DATABASE_URI)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
