from fastapi import APIRouter

from core.db import db

router = APIRouter()


@router.get("/")
async def index():
    return "Добро пожаловать на сервис аналитики!"


@router.get("/info")
async def info():
    return await db.get_info_all_users()
