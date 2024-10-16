import asyncio

from utils import crud


async def main():
    # await crud.insert_user("jacob", "jacob@example.fake", 33, "dogs.pdf")
    # await crud.update_user(user_id=7, number_upload_files=34, name_top_file="it.doc")

    # users = await crud.get_info_all_users()
    # print(users)

    users = await crud.get_info_all_users_by_top_file("dogs.pdf")
    print(users)


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
