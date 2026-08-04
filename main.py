from fastapi import FastAPI, HTTPException, status
import uvicorn
from schemas import STaskAdd, STask

app = FastAPI(
    title="Task Manager APIhjbhjbhj",
    description="Учебное приложение для курса bddbbfbffbпо FastAPI",
    version="1.0.0"
)

tasks = []

@app.get("/")
async def root():
    return {"me": "Hello World"}

@app.get("/tasks/{task_id}", response_model=STask)
async def read_user(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {task_id} не найдена"
    )

   
@app.post("/tasks", response_model=STask, status_code=status.HTTP_201_CREATED)
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)