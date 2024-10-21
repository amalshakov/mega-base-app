from pydantic import EmailStr
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from core.log import get_logger


logger = get_logger()


class DB:
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

    async def insert_user(
            self,
            username: str,
            email: EmailStr,
            number_upload_files: int = 0,
            name_top_file: str = None,
    ):
        query = text(
            "INSERT INTO users (username, email, number_upload_files, name_top_file) "
            "VALUES (:username, :email, :number_upload_files, :name_top_file)"
            ";"
        )
        async with self.engine.begin() as conn:
            try:
                await conn.execute(
                    query,
                    {
                        "username": username,
                        "email": email,
                        "number_upload_files": number_upload_files,
                        "name_top_file": name_top_file,
                    },
                )
                logger.info(f"Пользователь '{username}' с email '{email}' успешно добавлен.")
            except SQLAlchemyError as error:
                logger.info(f"Ошибка при добавлении пользователя '{username}' с email '{email}': '{error}'")
                raise

    async def insert_users(
            self,
            users: list[dict[str, int]],
    ):
        query = text(
            "INSERT INTO users (username, email, number_upload_files, name_top_file) "
            "VALUES (:username, :email, :number_upload_files, :name_top_file)"
            ";"
        )
        async with self.engine.begin() as conn:
            for user in users:
                try:
                    await conn.execute(
                        query,
                        {
                            "username": user["username"],
                            "email": user["email"],
                            "number_upload_files": user.get("number_upload_files"),
                            "name_top_file": user.get("name_top_file"),
                        },
                    )
                    logger.info(f"Пользователь '{user['username']}' с email '{user['email']}' успешно добавлен.")
                except SQLAlchemyError as error:
                    logger.error(f"Ошибка при вставке пользователя '{user['username']}' с email '{user['email']}': {error}")
                    raise

    async def update_user(
            self,
            user_id: int, **kwargs,
    ):
        async with self.engine.begin() as conn:
            for key, value in kwargs.items():
                if value is not None:
                    query = text(
                        f"UPDATE users "
                        f"SET {key}='{value}' "
                        f"WHERE id={user_id}"
                        f";"
                    )
                else:
                    query = text(
                        f"UPDATE users "
                        f"SET {key}=NULL "
                        f"WHERE id={user_id}"
                        f";"
                    )
                try:
                    await conn.execute(query)
                    logger.info(f"Пользователь с id '{user_id}' -> успешно обновлено поле '{key}' на значение '{value}'")
                except SQLAlchemyError as error:
                    logger.error(f"Пользователь с id '{user_id}' -> ошибка обновления поля '{key}' на значение '{value}'. Ошибка: '{error}'")
                    raise

    async def get_info_all_users(self):
        query = text(
            "SELECT id, username, email, number_upload_files, name_top_file "
            "FROM users"
            ";"
        )
        async with self.engine.begin() as conn:
            try:
                result = await conn.execute(query)
                logger.info("Запрос к БД на получение всех пользователей выполнен успешно")
            except SQLAlchemyError as error:
                logger.error(f"Ошибка при запросе к БД на получение всех пользователей. Ошибка: '{error}'")
                raise
            users = result.mappings().fetchall()
            return users

    async def get_info_all_users_by_top_file(
            self,
            name_top_file,
    ):
        query = text(
            f"SELECT id, username, email, number_upload_files, name_top_file "
            f"FROM users "
            f"WHERE name_top_file = '{name_top_file}'"
            f";"
        )
        async with self.engine.begin() as conn:
            try:
                result = await conn.execute(query, {"name_top_file": name_top_file})
                logger.info(f"Запрос к БД на получение пользователей с полем 'name_top_file': '{name_top_file}' выполнен успешно")
            except SQLAlchemyError as error:
                logger.error(f"Ошибка при запросе к БД на получение всех пользователей с полем 'name_top_file': '{name_top_file}'. Ошибка: '{error}'")
                raise
            users = result.mappings().fetchall()
            return users


db = DB(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
)
