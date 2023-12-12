from fastapi import APIRouter, Depends
from app import models
from app.services import HouseService
from app.schemas.house_schema import ResponseHouse, BaseHouse, FindHouse
from typing import List, Optional, Annotated
from fastapi_pagination import Page
from fastapi_pagination.ext.mongoengine import paginate

router = APIRouter(tags=["house"], prefix="/house")


@router.get("/", response_model=Page[ResponseHouse])
async def house(
    house_service: HouseService = Depends(HouseService),
    find_house: FindHouse = Depends(),
):
    houses = house_service.get_list()
    return paginate(houses)


@router.post("/create", response_model=ResponseHouse)
async def create_house(
    house: BaseHouse, house_service: HouseService = Depends(HouseService)
):
    house = house_service.create(house)
    return house


@router.patch("/{house_id}", response_model=ResponseHouse)
async def update_house(
    house_id: str, house: BaseHouse, house_service: HouseService = Depends(HouseService)
):
    house = house_service.patch(house_id, house)
    return house


@router.delete("/{house_id}", response_model=BaseHouse)
async def delete_house(
    house_id: str, house_service: HouseService = Depends(HouseService)
):
    house = house_service.delete_by_id(house_id)
    return house
