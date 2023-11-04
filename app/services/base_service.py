from pydantic import BaseModel
from mongoengine import Document, QuerySet
from typing import Any
from app.repository import BaseRepository
from bson import ObjectId


class BaseService:
    def __init__(self, repository: BaseRepository):
        self._repository: BaseRepository = repository

    def get_list(self, schema: BaseModel | None = None, **kwargs: int) -> QuerySet:
        return self._repository.get_by_options(schema, **kwargs)

    def get_by_id(self, id: str | ObjectId) -> Document:
        return self._repository.get_by_id(id)

    def add(self, schema: BaseModel | None = None, **kwargs: int) -> Document:
        return self._repository.create(schema, **kwargs)

    def patch(
        self, id: str | ObjectId, schema: BaseModel | None = None, **kwargs: int
    ) -> Document:
        return self._repository.update(id, schema, **kwargs)

    def patch_attr(self, id: str | ObjectId, attr: str, value: Any) -> Document:
        return self._repository.update_attr(id, attr, value)

    def put_update(
        self, id: str | ObjectId, schema: BaseModel | None = None, **kwargs: int
    ) -> Document:
        return self._repository.whole_update(id, schema, **kwargs)

    def delete_by_id(self, id: str | ObjectId) -> Document:
        return self._repository.delete_by_id(id)
