from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api.v1.views.endpoints import router as router_v1
from config import settings
from core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await db_helper.create_tables()
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(router_v1)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
