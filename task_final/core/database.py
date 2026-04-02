from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import DB_URL

Base = declarative_base()
engine = create_async_engine(DB_URL)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# функция которая создает подключение к бд
async def get_db():
    async with SessionLocal() as db:
        yield db