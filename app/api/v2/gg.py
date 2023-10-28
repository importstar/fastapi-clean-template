from fastapi import APIRouter
from loguru import logger

router = APIRouter(tags=["gg"], prefix="/gg")


@router.get("/")
async def gg():
    return {"msg": "gg"}
