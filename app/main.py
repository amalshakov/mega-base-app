from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from config import settings
from utils import crud, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await db_helper.create_tables()
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
