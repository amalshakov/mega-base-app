from fastapi import APIRouter

from core import crud

router = APIRouter()


@router.get("/")
async def index():
    return "Добро пожаловать на сервис аналитики!"


@router.get("/info")
async def info():
    return await crud.get_info_all_users()
