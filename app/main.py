from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api.v1.views.endpoints import router as router_v1
from config import settings
from core.db import db
from core.utils import get_email_from_full_name
from core.utils import validate_email


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # await db.create_tables()
    yield
    # shutdown
    await db.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(router_v1)

if __name__ == "__main__":
    while True:
        snp = input("Введите ФИО (в формате: Фамилия Имя Отчество): ")
        print(get_email_from_full_name(snp))
    # uvicorn.run(
    #     "main:main_app",
    #     host=settings.run.host,
    #     port=settings.run.port,
    #     reload=True,
    # )
