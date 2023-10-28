from bson import ObjectId
from typing import Any, Optional, Union, List
import datetime
from pydantic_core import CoreSchema, core_schema
from pydantic_core.core_schema import (
    ValidationInfo,
    str_schema,
)
from bson.errors import InvalidId
from pydantic import (
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    BaseModel,
    Field,
    ConfigDict,
)
from pydantic.json_schema import JsonSchemaValue


class PydanticObjectId(ObjectId):
    """
    Object Id field. Compatible with Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _: ValidationInfo):
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        try:
            return PydanticObjectId(v)
        except InvalidId:
            raise ValueError("Id must be of type PydanticObjectId")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:  # type: ignore
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler  # type: ignore
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(
            type="string",
            example="5eb7cf5a86d9755df3a6c593",
        )
        return json_schema


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,  # from orm_mode
        validate_default=True,
    )


class BaseSchemaInfo(BaseSchema):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
        serialization_alias="id",
    )

    created_date: datetime.datetime
    updated_date: datetime.datetime


class FindBase(BaseSchema):
    ...


class SearchOptions(FindBase):
    ...


class FindResult(BaseSchema):
    ...


class FindDateRange(BaseSchema):
    ...
