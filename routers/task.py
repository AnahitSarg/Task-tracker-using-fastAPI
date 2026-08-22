from fastapi import APIRouter, HTTPException, status, Depends
from schemas.task import STaskAdd, STask
from database import SessionDep 

from typing import Annotated
from sqlalchemy import select, delete
from models.tasks import TasksModel



router = APIRouter(
    #Роутер сам приклеит префикс /tasks ко всем путям внутри себя.
    prefix="/tasks",
    tags=["Задачи"]
)


@router.get("")
async def get_tasks(session: SessionDep):
    query = select(TasksModel)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/{task_id}", response_model=STask)
async def read_user(task_id: int, session: SessionDep):
    #for task in tasks:
    #    if task["id"] == task_id:
    #        return task
    query = select(TasksModel).where(TasksModel.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    #кроткий вариант
    #task = await session.get(TasksModel, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task

   
@router.post("", response_model=STask, status_code=status.HTTP_201_CREATED)
async def create_task(task: STaskAdd, session: SessionDep):
    # 1. Превращаем Pydantic-модель в словарь
    #task_dict = task.model_dump()
    # 2. Генерируем ID (длина списка + 1)
    #task_id = len(tasks) + 1
    #task_dict["id"] = task_id
    # 3. Сохраняем в список
    #tasks.append(task_dict)
    # 4. Возвращаем словарь. 
    # FastAPI сам превратит его в схему STask (проверит наличие ID)
    #return task_dict

    #1.Превращаем Pydantic-модель в словарь
    #  ** - это распаковка словаря
    new_task =TasksModel(**task.model_dump())
    #2. Добавляем в сессию
    session.add(new_task)
    #3. Сохраняем на диск
    await session.commit()
    #4. Обновляем объект (получаем выданный ID)
    await session.refresh(new_task)
    #5. Возвращаем объект БД. Pydantic сам превратит его в JSON
    return new_task




@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: SessionDep):
    #for index, task in enumerate(tasks):
    #    if task["id"] == task_id:
    #        tasks.pop(index)
    #        return
    deleted_task = delete(TasksModel).where(TasksModel.id == task_id)
    result = await session.execute(deleted_task)
    await session.commit()

    #Проверяем, был ли удалён хотя бы один ряд
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    return