import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api.v1.views.endpoints import router as router_v1
from config import settings
from core.db import db
from core.utils import get_email_from_full_name
from users_for_db import USERS_FOR_DB


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(router_v1)

async def run_fastapi():
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

async def main():
    count = 5
    while count != 0:
        print(f"Вам нужно создать email - {count} шт.")
        fml = input("Введите ФИО в формате: Фамилия Имя Отчество: ")
        email = get_email_from_full_name(fml)
        if email:
            USERS_FOR_DB[count-1]["email"] = email
            count -= 1

    print("Поздравляем! Вы молодец! Вы заполнили все email'ы. Спасибо!")
    print("Массив с пользователями сформирован:")
    for user in USERS_FOR_DB:
        print(user)

    await db.create_tables()
    await db.insert_users(USERS_FOR_DB)

    print("Запускаем FastAPI?")
    user_input = ""
    while user_input not in ["да", "нет"]:
        user_input = input("Введите 'да' или 'нет': ").strip().lower()
    if user_input == "нет":
        print("До свидания!")
        return

    print("Запуск FastAPI!!!")
    print("Вы можете перейти на следующие страницы:")
    print("Главная страница -> http://127.0.0.1:8000/")
    print("Топ пользователей по загрузке файлов -> http://127.0.0.1:8000/info")

    await run_fastapi()


if __name__ == "__main__":
    asyncio.run(main())
