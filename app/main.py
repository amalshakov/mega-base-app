from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from config import settings
from utils import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await db_helper.create_tables()
    # await db_helper.insert_user("kate", "kate@example.fake", 10, "cats.pdf")
    # await db_helper.update_user(user_id=2, number_upload_files=999)
    # await db_helper.get_info_all_users()
    # await db_helper.get_info_all_users_by_top_file("cats.pdf")
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
