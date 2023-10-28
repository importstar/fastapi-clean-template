from fastapi import APIRouter, Depends
from app import models
from app import schemas
from app import services
from app.schemas.house_schema import OutHouse
from typing import List, Optional
from fastapi_pagination import Page
from fastapi_pagination.ext.mongoengine import paginate

router = APIRouter(tags=["house"], prefix="/house")


@router.get("/", response_model=Page[OutHouse])
async def house():
    houses = services.HouseService().get_list()
    return paginate(houses)


@router.post("/create", response_model=schemas.OutHouse)
async def create_house(house: schemas.BaseHouse):
    item = services.HouseService().add(house)
    return schemas.OutHouse(**item.to_mongo())


@router.patch("/{house_id}", response_model=schemas.OutHouse)
async def update_house(
    house_id: str,
    house: schemas.BaseHouse,
):
    item = services.HouseService().patch(house_id, house)
    return schemas.OutHouse(**item.to_mongo())


@router.delete("/{house_id}", response_model=schemas.BaseHouse)
async def delete_house(house_id: str):
    item = services.HouseService().delete_by_id(house_id)
    return schemas.BaseHouse(**item.to_mongo())
