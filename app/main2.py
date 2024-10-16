import asyncio

from utils import crud


USERS_FOR_DB = [
    {
        "username": "jessika",
        "email": "jessika@example.fake",
        "number_upload_files": 27,
        "name_top_file": "encyclopedia.txt"
    },
    {
        "username": "john",
        "email": "john@example.fake",
        "number_upload_files": 805,
        "name_top_file": "encyclopedia.txt"
    },
    {
        "username": "alexander",
        "email": "alexander@example.fake",
        "number_upload_files": 2029,
        "name_top_file": "cats.jpeg"
    },
    {
        "username": "ben",
        "email": "ben@example.fake",
        "number_upload_files": 72,
        "name_top_file": "cats.jpeg"
    },
    {
        "username": "julie",
        "email": "julie@example.fake",
        "number_upload_files": 7828,
        "name_top_file": "all stars.jpeg"
    },
]


async def main():
    # await crud.insert_user("jacob", "jacob@example.fake", 33, "dogs.pdf")
    await crud.insert_users(USERS_FOR_DB)

    # await crud.update_user(user_id=7, number_upload_files=34, name_top_file="it.doc")

    # users = await crud.get_info_all_users()
    # print(users)

    # users = await crud.get_info_all_users_by_top_file("dogs.pdf")
    # print(users)


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
