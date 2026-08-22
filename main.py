from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from routers.task import router as tasks_router
from models.tasks import TasksModel #Нужно, чтобы таблица зарегистрировалась
from database import engine, Model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- КОД ПРИ СТАРТЕ ---
    # Мы обращаемся к движку и просим создать все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    
    print("База данных готова к работе")
    
    yield  # Разделяет старт и выключение
    
    # --- КОД ПРИ ВЫКЛЮЧЕНИИ ---
    print("Выключение сервера")





# Передаем lifespan в приложение
app = FastAPI(lifespan=lifespan)
# Подключаем роутер к приложению
app.include_router(tasks_router)

@app.get("/")
async def root():
    return {"me": "Hello World"}


if __name__ == "__main__":
    import sys
    print("Используемый интерпретатор:", sys.executable)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)