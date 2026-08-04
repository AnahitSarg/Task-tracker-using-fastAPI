import uvicorn

from fastapi import FastAPI

app = FastAPI(
    title="Task Manager APIhjbhjbhj",
    description="Учебное приложение для курса bddbbfbffbпо FastAPI",
    version="1.0.0"
)

fake_tasks_db = [
    {"task_id": 1, "task_name": "Изучить Python"},
    {"task_id": 2, "task_name": "Подключить Базу Данных"},
    {"task_id": 3, "task_name": "Выучить FastAPI"},
]

@app.get("/")
async def root():
    return {"me": "Hello World"}

@app.get("/tasks/{task_id}")
async def read_user(task_id: int):
    for task in fake_tasks_db:
        if task["task_id"] == task_id:
            return task
        
    return {}
    # Если не нашли — выдаем ошибку 404
    #raise HTTPException(status_code=404, detail="Task not found")

# Добавляем этот блок в конец файла
if __name__ == "__main__":
    # Обратите внимание: имя файла передается как строка
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)