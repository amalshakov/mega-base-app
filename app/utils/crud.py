from pydantic import EmailStr
from sqlalchemy import text

from . import db_helper

async def insert_user(
        username: str,
        email: EmailStr,
        number_upload_files: int = 0,
        name_top_file: str = None,
):
    insert_query = """
    INSERT INTO users (username, email, number_upload_files, name_top_file)
    VALUES (:username, :email, :number_upload_files, :name_top_file);
    """
    async with db_helper.engine.begin() as conn:
        await conn.execute(
            text(insert_query),
            {
                "username": username,
                "email": email,
                "number_upload_files": number_upload_files,
                "name_top_file": name_top_file,
            },
        )


async def insert_users(users: list[dict[str, int]]):
    insert_query = """
    INSERT INTO users (username, email, number_upload_files, name_top_file)
    VALUES (:username, :email, :number_upload_files, :name_top_file);
    """
    async with db_helper.engine.begin() as conn:
        for user in users:
            await conn.execute(
                text(insert_query),
                {
                    "username": user["username"],
                    "email": user["email"],
                    "number_upload_files": user["number_upload_files"],
                    "name_top_file": user["name_top_file"],
                },
            )


async def update_user(
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

    async with db_helper.engine.begin() as conn:
        await conn.execute(
            text(update_query),
            update_values,
        )


async def get_info_all_users():
    select_query = """
    SELECT id, username, email, number_upload_files, name_top_file
    FROM users;
    """
    async with db_helper.engine.begin() as conn:
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


async def get_info_all_users_by_top_file(name_top_file):
    select_query = """
    SELECT id, username, email, number_upload_files, name_top_file
    FROM users
    WHERE name_top_file = :name_top_file;
    """
    async with db_helper.engine.begin() as conn:
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