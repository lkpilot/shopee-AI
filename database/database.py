from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DB_URL = os.getenv("DB_URL")

engine = create_async_engine(DB_URL, pool_pre_ping=True, echo=True)

Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()