from app.schemas.base_schema import BaseSchema, BaseSchemaInfo, FindBase
from pydantic import BaseModel, Field
from typing import Optional
from app.utils import AllOptional, PydanticObjectId
import datetime


class BaseHouse(BaseSchema):
    name: str
    width: float
    height: float
    volume: float


class FindHouse(FindBase):
    name: Optional[str] = None


class ResponseHouse(BaseHouse):
    id: PydanticObjectId = Field(alias="_id", serialization_alias="id")
