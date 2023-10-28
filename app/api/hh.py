from fastapi import APIRouter
from loguru import logger

router = APIRouter(tags=["hh"], prefix="/hh")


@router.get("/")
async def hh():
    logger.debug("hh")
    return {"msg": "hhhh"}
