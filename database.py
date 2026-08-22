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
#По умолчанию SQLAlchemy после сохранения (commit) "протухает" все объекты. 
# Если вы захотите прочитать поле task.name после сохранения, она полезет в базу обновлять данные. 
# В асинхронном режиме это может вызвать ошибку, если сессия уже закрыта. 
# False отключает это поведение — данные остаются в памяти.


# 3. Создание фабрики сессий
new_session = async_sessionmaker(engine, expire_on_commit=False)

# 4. Базовый класс для моделей
# MappedAsDataclass - нужен для удобной работы с типами (новинка 2.0)
# Простой синтаксис типов (int, str) и без необходимости написания методов __init__ вручную
class Model(MappedAsDataclass, DeclarativeBase):
    pass


async def get_db():
    async with new_session() as session:
        yield session

        
# Создаем аннотацию для типа
# Аннотация говорит: "Это переменная типа AsyncSession, 
# и чтобы её получить, нужно выполнить функцию get_db"
SessionDep = Annotated[AsyncSession, Depends(get_db)]


