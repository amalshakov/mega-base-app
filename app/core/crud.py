from pydantic import EmailStr
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from core.log import get_logger
from core.db_helper import db_helper

logger = get_logger()


async def insert_user(
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
    async with db_helper.engine.begin() as conn:
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


async def insert_users(users: list[dict[str, int]]):
    query = text(
        "INSERT INTO users (username, email, number_upload_files, name_top_file) "
        "VALUES (:username, :email, :number_upload_files, :name_top_file)"
        ";"
    )
    async with db_helper.engine.begin() as conn:
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


async def update_user(user_id: int, **kwargs):
    async with db_helper.engine.begin() as conn:
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


async def get_info_all_users():
    query = text(
        "SELECT id, username, email, number_upload_files, name_top_file "
        "FROM users"
        ";"
    )
    async with db_helper.engine.begin() as conn:
        try:
            result = await conn.execute(query)
            logger.info("Запрос к БД на получение всех пользователей выполнен успешно")
        except SQLAlchemyError as error:
            logger.error(f"Ошибка при запросе к БД на получение всех пользователей. Ошибка: '{error}'")
            raise
        users = result.mappings().fetchall()
        return users


async def get_info_all_users_by_top_file(name_top_file):
    query = text(
        f"SELECT id, username, email, number_upload_files, name_top_file "
        f"FROM users "
        f"WHERE name_top_file = '{name_top_file}'"
        f";"
    )
    async with db_helper.engine.begin() as conn:
        try:
            result = await conn.execute(query, {"name_top_file": name_top_file})
            logger.info(f"Запрос к БД на получение всех пользователей выполнен успешно, для пользователей с полем 'name_top_file': '{name_top_file}'")
        except SQLAlchemyError as error:
            logger.error(f"Ошибка при запросе к БД на получение всех пользователей с полем 'name_top_file': '{name_top_file}'. Ошибка: '{error}'")
            raise
        users = result.mappings().fetchall()
        return users