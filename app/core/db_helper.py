from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from core.log import get_logger


logger = get_logger()


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def create_tables(self):
        query = text(
            "CREATE TABLE IF NOT EXISTS users "
            "("
            "id SERIAL PRIMARY KEY, "
            "username VARCHAR(50) NOT NULL, "
            "email VARCHAR(100) NOT NULL UNIQUE, "
            "number_upload_files INT, "
            "name_top_file VARCHAR(255)"
            ")"
            ";"
        )
        async with self.engine.begin() as conn:
            try:
                await conn.execute(query)
                logger.info("Таблица 'users' успешно создана или уже существует.")
            except SQLAlchemyError as error:
                logger.error(f"Ошибка при создании таблицы: '{error}'")
                raise


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
)
