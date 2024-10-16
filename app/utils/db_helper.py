from pydantic import EmailStr
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.sql.functions import session_user
from typing_extensions import reveal_type

from config import settings


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
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            number_upload_files INT,
            name_top_file VARCHAR(255)
        );
        """
        async with self.engine.begin() as conn:
            await conn.execute(text(create_table_query))

    async def insert_user(
        self,
        username: str,
        email: EmailStr,
        number_upload_files: int = 0,
        name_top_file: str = None,
    ):
        insert_query = """
        INSERT INTO users (username, email, number_upload_files, name_top_file)
        VALUES (:username, :email, :number_upload_files, :name_top_file);
        """
        async with self.engine.begin() as conn:
            await conn.execute(
                text(insert_query),
                {
                    "username": username,
                    "email": email,
                    "number_upload_files": number_upload_files,
                    "name_top_file": name_top_file,
                },
            )

    async def update_user(
        self,
        user_id,
        username: str = None,
        email: EmailStr = None,
        number_upload_files: int = None,
        name_top_file: str = None,
    ):
        if not any([user_id, username, email, number_upload_files, name_top_file]):
            raise ValueError("No data for update user.")

        # example SQL query
        # """
        # UPDATE users
        # SET username = :username, email = :email, number_upload_files = :number_upload_files ...
        # WHERE id = :user_id
        # """

        update_query = "UPDATE users SET "
        update_values = {}

        set_part = []
        if username is not None:
            set_part.append("username = :username")
            update_values["username"] = username
        if email is not None:
            set_part.append("email = :email")
            update_values["email"] = email
        if number_upload_files is not None:
            set_part.append("number_upload_files = :number_upload_files")
            update_values["number_upload_files"] = number_upload_files
        if name_top_file is not None:
            set_part.append("name_top_file = :name_top_file")
            update_values["name_top_file"] = name_top_file

        update_query += ", ".join(set_part)
        update_query += " WHERE id = :user_id"
        update_values["user_id"] = user_id

        async with self.engine.begin() as conn:
            await conn.execute(
                text(update_query),
                update_values,
            )

    async def get_info_all_users(self):
        select_query = """
        SELECT id, username, email, number_upload_files, name_top_file
        FROM users;
        """
        async with self.engine.begin() as conn:
            result = await conn.execute(text(select_query))
            rows = result.fetchall()

        users = [
            {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "number_upload_files": row[3],
                "name_top_file": row[4],
            }
            for row in rows
        ]
        return users
        # print(users)

    async def get_info_all_users_by_top_file(self, name_top_file):
        select_query = """
        SELECT id, username, email, number_upload_files, name_top_file
        FROM users
        WHERE name_top_file = :name_top_file;
        """
        async with self.engine.begin() as conn:
            result = await conn.execute(text(select_query), {"name_top_file": name_top_file})
            rows = result.fetchall()

        users = [
            {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "number_upload_files": row[3],
                "name_top_file": row[4],
            }
            for row in rows
        ]
        return users
        # print(users)


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
)
