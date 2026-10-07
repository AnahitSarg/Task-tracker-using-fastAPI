from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


# 1. Настройка URL
# Файл tasks.db создастся в корне проекта
DATABASE_URL = "sqlite+aiosqlite:///tasks.db"

# 2. Создание движка
engine = create_async_engine(DATABASE_URL)

# 3. Создание фабрики сессий
new_session = async_sessionmaker(engine, expire_on_commit=False)

# 4. Базовый класс для моделей
class Model(MappedAsDataclass, DeclarativeBase):
    pass


async def get_db():
    async with new_session() as session:
        yield session

        
SessionDep = Annotated[AsyncSession, Depends(get_db)]


