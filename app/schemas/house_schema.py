from app.schemas.base_schema import BaseSchema, BaseSchemaInfo
from pydantic import BaseModel, Field
from typing import Optional
from app.utils import AllOptional
import datetime


class BaseHouse(BaseSchema):
    name: str | None = None
    width: float | None = None
    height: float | None = None
    volume: float | None = None


class OutHouse(BaseHouse, BaseSchemaInfo):
    ...
