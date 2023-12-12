from app.repository.house_repository import HouseRepository
from app.services.base_service import BaseService
from app.schemas.house_schema import FindHouse
from app import models
from mongoengine import QuerySet


class HouseService(BaseService):
    def __init__(self):
        house_repository = HouseRepository()
        super().__init__(house_repository)

    def find_house(self, schema: FindHouse) -> QuerySet:
        schema_dict = schema.model_dump(exclude_defaults=True)
        query_schema_dict = {}
        if "name" in schema_dict:
            query_schema_dict["name__icontains"] = schema_dict.pop("name")

        return self.get_list(**query_schema_dict)
