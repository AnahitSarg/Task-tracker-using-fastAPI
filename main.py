from fastapi import FastAPI
import uvicorn
from routers.task import router as tasks_router

app = FastAPI(
    title="Task Manager APIhjbhjbhj",
    description="Учебное приложение для FastAPI",
    version="1.0.0"
)

# Подключаем роутер к приложению
app.include_router(tasks_router)

@app.get("/")
async def root():
    return {"me": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)