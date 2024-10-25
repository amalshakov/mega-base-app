import os
import asyncio

from dotenv import load_dotenv

from core.db import db
from core import utils
from core.regex import validate_email
from core.utils import get_email_from_full_name

load_dotenv()

USERS_FOR_DB = [
    {
        "username": "jessika",
        "email": os.getenv("EMAIL_JESSIKA"),
        "number_upload_files": 27,
        "name_top_file": "encyclopedia.txt"
    },
    {
        "username": "john",
        "email": os.getenv("EMAIL_JOHN"),
        "number_upload_files": 805,
        "name_top_file": "encyclopedia.txt"
    },
    {
        "username": "alexander",
        "email": os.getenv("EMAIL_ALEXANDER"),
        "number_upload_files": 2029,
        "name_top_file": "cats.jpeg"
    },
    {
        "username": "ben",
        "email": os.getenv("EMAIL_BEN"),
        "number_upload_files": 72,
        "name_top_file": "cats.jpeg"
    },
    {
        "username": "julie",
        "email": os.getenv("EMAIL_JULIE"),
        "number_upload_files": 7828,
        "name_top_file": "all stars.jpeg"
    },
]


async def main():

    # await db.create_tables()
    # await db.insert_user("jorgie", "jorgie@example.fake", 72, "dogs.pdf")
    await db.insert_users(USERS_FOR_DB)

    # await db.update_user(user_id=1, username=None)
    # await db.update_user(user_id=1, email=None)
    # await db.update_user(user_id=1, number_upload_files=99913)


    # users = await db.get_info_all_users()
    # print(users)

    # users = await db.get_info_all_users_by_top_file("cats.jpeg")
    # print(users)

    # sorted_users_by_uploads = utils.sort_users_by_uploads(await db.get_info_all_users())
    # print(sorted_users_by_uploads)

    # while True:
    #     email = input("Введите email: ")
    #     validate_email(email)
    #     snp = input("Введите ФИО (в формате: Фамилия Имя Отчество): ")
    #     print(get_email_from_full_name(snp))


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
