from pydantic import BaseModel

# 1. Базовый класс (общие поля)
class STaskBase(BaseModel):
    name: str
    description: str | None = None

# 2. Класс для создания (ничего не добавляет, просто копирует базу)
class STaskAdd(STaskBase):
    pass

# 3. Класс для чтения (добавляет id)
class STask(STaskBase):
    id: int