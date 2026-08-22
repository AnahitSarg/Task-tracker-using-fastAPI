from fastapi import APIRouter, HTTPException, status
from schemas.task import STaskAdd, STask
from database import SessionDep 

from repository import TaskRepository 


router = APIRouter(
    #Роутер сам приклеит префикс /tasks ко всем путям внутри себя.
    prefix="/tasks",
    tags=["Задачи"]
)


@router.get("")
async def get_tasks(session: SessionDep):
    tasks = await TaskRepository.find_all(session)
    return tasks

@router.get("/{task_id}", response_model=STask)
async def read_user(task_id: int, session: SessionDep):
    task = await TaskRepository.find_by_id(task_id, session)


    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task

   
@router.post("", response_model=STask, status_code=status.HTTP_201_CREATED)
async def create_task(task: STaskAdd, session: SessionDep):

    task_model = await TaskRepository.add_one(task, session)
    return task_model




@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: SessionDep):
    deleted = await TaskRepository.remove_by_id(task_id, session)
    #Проверяем, был ли удалён хотя бы один ряд
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    return