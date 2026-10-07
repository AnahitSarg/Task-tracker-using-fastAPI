from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.tasks import TasksModel
from schemas.task import STaskAdd
class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd, session: AsyncSession) -> TasksModel:
        #1.Превращаем Pydantic-модель в словарь, создаем объект модели
        #  ** - это распаковка словаря
        new_task =TasksModel(**data.model_dump())
        #2. Добавляем в сессию
        session.add(new_task)
        #3. Сохраняем на диск
        await session.commit()
        #4. Обновляем объект (получаем выданный ID)
        await session.refresh(new_task)
        #5. Возвращаем объект БД. Pydantic сам превратит его в JSON
        return new_task

    @classmethod
    async def find_all(cls, session: AsyncSession):
        query = select(TasksModel)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_by_id(cls, id: int, session: AsyncSession):
        query = select(TasksModel).where(TasksModel.id == id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()
        return task   

    @classmethod
    async def remove_by_id(cls, id: int, session: AsyncSession):
        deleted_task = delete(TasksModel).where(TasksModel.id == id)
        result = await session.execute(deleted_task)
        await session.commit()
        return result.rowcount > 0
