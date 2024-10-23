from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from core.db import db
from core.utils import sort_users_by_uploads

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
async def index():
    return "Добро пожаловать на сервис аналитики!"


@router.get("/info", response_class=PlainTextResponse)
async def info():
    users = await db.get_info_all_users()
    sorted_users_by_uploads = sort_users_by_uploads(users)
    count_upload_files_by_user3 = sorted_users_by_uploads[2]["number_upload_files"]

    top_users = [user for user in sorted_users_by_uploads if user["number_upload_files"] >= count_upload_files_by_user3]

    result = "Топ пользователей по выгрузке файлов:\n\n"

    for i, user in enumerate(top_users, 1):
        result += (
            f"{i} место - {user['username']}\n"
            f"Количество скачанных файлов - {user['number_upload_files']}\n"
            f"TOP file - {user['name_top_file']}\n\n"
        )

    return result
