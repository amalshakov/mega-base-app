from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.config import db
from app.core.utils import sort_users_by_uploads

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
async def index():
    """Главная страница сервиса аналитики."""
    return "Добро пожаловать на сервис аналитики!"


@router.get("/info", response_class=PlainTextResponse)
async def info():
    """
    Получение информации о пользователях и их активности.

    Эта функция извлекает информацию о всех пользователях из базы данных,
    сортирует их по количеству загруженных файлов и формирует список
    топ пользователей, которые загрузили больше файлов.

    """
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
