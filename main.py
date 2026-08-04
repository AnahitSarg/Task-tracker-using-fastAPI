from fastapi import FastAPI
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

@app.get("/tasks/{task_id}")
async def read_user(task_id: int):
    for task in tasks:
        if task["task_id"] == task_id:
            return task
        
    return {}
    # Если не нашли — выдаем ошибку 404
    #raise HTTPException(status_code=404, detail="Task not found")


   
@app.post("/tasks", response_model=STask)
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