from fastapi import APIRouter, HTTPException, status
from schemas import STaskAdd, STask

router = APIRouter(
    #Роутер сам приклеит префикс /tasks ко всем путям внутри себя.
    prefix="/tasks",
    tags=["Задачи"]
)

tasks = []

@router.get("")
async def get_tasks():
    return tasks 

@router.get("/{task_id}", response_model=STask)
async def read_user(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {task_id} не найдена"
    )

   
@router.post("", response_model=STask, status_code=status.HTTP_201_CREATED)
async def create_task(task: STaskAdd):
    # 1. Превращаем Pydantic-модель в словарь
    task_dict = task.model_dump()
    
    # 2. Генерируем ID (длина списка + 1)
    task_id = len(tasks) + 1
    task_dict["id"] = task_id
    
    # 3. Сохраняем в список
    tasks.append(task_dict)
    
    # 4. Возвращаем словарь. 
    # FastAPI сам превратит его в схему STask (проверит наличие ID)
    return task_dict

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    #Если цикл прошел и ничего не нашли
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача не найдена"
    )
