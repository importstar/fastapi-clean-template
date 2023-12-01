from typing import Any, Optional, Annotated, TypeVar, Generic, Union, get_args

from bson import ObjectId, DBRef
from bson.errors import InvalidId
from mongoengine import Document
from mongoengine.base.metaclasses import TopLevelDocumentMetaclass

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, BaseModel
from pydantic.json_schema import JsonSchemaValue
from pydantic.main import _model_construction
from pydantic.functional_validators import BeforeValidator
from pydantic_core import CoreSchema, core_schema

from app.models import cls_documents
from app.core.exceptions import ValidationError

from loguru import logger


class AllOptional(_model_construction.ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            optionals = {
                key: Optional[value] if not key.startswith("__") else value
                for key, value in base.__annotations__.items()
            }
            annotations.update(optionals)

        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


PyObjectId = Annotated[str, BeforeValidator(str)]
T = TypeVar("T")


class PydanticObjectId(ObjectId):
    """
    Object Id field. Compatible with Pydantic.
    """

    @classmethod
    def validate(cls, v, _: core_schema.ValidationInfo):
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        try:
            if isinstance(v, DBRef):
                return PydanticObjectId(v.id)

            return PydanticObjectId(v)
        except InvalidId:
            raise ValueError("Id must be of type PydanticObjectId")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:  # type: ignore
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=core_schema.str_schema(),
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


class PydanticDBRef(DBRef):
    """
    DBRef field. Compatible with Pydantic.
    """

    @classmethod
    def validate(cls, v, _: core_schema.ValidationInfo):
        print(v.collection)
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        try:
            return PydanticObjectId(v.id)
        except InvalidId:
            raise ValueError("Reference must be of type PydanticDBRef")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:  # type: ignore
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler  # type: ignore
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(type="string", example="5eb7cf5a86d9755df3a6c593")
        return json_schema


class DeDBRef(Generic[T]):
    """Dereference DBRef bson object to a schema

    Usage:
    .. code-block:: python
        from user_schema import User

        user: DeDBRef[User] = Field(json_schema_extra="user_field")"""

    def __init__(self, document_class: BaseModel):
        self.document_class = document_class

    @classmethod
    def build_validation(cls, handler, source_type):
        def validate(v: Union[DBRef, T], validation_info: core_schema.ValidationInfo):
            document_class: BaseModel = get_args(source_type)[0]

            if isinstance(v, (dict, BaseModel)):
                return v

            if isinstance(v, Document):
                return document_class(**v.to_mongo())

            if isinstance(v, DBRef):
                for doc in cls_documents:
                    if isinstance(doc, TopLevelDocumentMetaclass):
                        if doc._get_collection_name() == v.collection:
                            try:
                                return document_class(
                                    **doc.objects.with_id(v.id).to_mongo()
                                )
                            except Exception as e:
                                raise ValidationError("Could not validate DBRef object")
            return None

        return validate

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(
                cls.build_validation(handler, source_type)
            ),
            json_schema=core_schema.typed_dict_schema(
                {"attr": core_schema.typed_dict_field(core_schema.str_schema())}
            ),
        )
