from fastapi import APIRouter

from core.db import db
from core.utils import sort_users_by_uploads

router = APIRouter()


@router.get("/")
async def index():
    return "Добро пожаловать на сервис аналитики!"


@router.get("/info")
async def info():
    users = await db.get_info_all_users()
    sorted_users_by_uploads = sort_users_by_uploads(users)
    return f"Топ пользователей по выгрузке файлов: {sorted_users_by_uploads}"
