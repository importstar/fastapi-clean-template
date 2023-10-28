from pydantic import BaseModel
from mongoengine import Document
from typing import Any
from app.repository import BaseRepository
from bson import ObjectId


class BaseService:
    def __init__(self, repository: BaseRepository) -> None:
        self._repository: BaseRepository = repository()

    def get_list(self, schema: BaseModel | None = None, **kwargs: int):
        return self._repository.read_by_options(schema, **kwargs)

    def get_by_id(self, id: str | ObjectId):
        return self._repository.read_by_id(id)

    def add(self, schema: BaseModel | None = None, **kwargs: int):
        return self._repository.create(schema, **kwargs)

    def patch(self, id: str | ObjectId, schema: BaseModel | None = None):
        return self._repository.update(id, schema)

    def patch_attr(self, id: str | ObjectId, attr: str, value: Any):
        return self._repository.update_attr(id, attr, value)

    def put_update(self, id: str | ObjectId, schema: BaseModel | None = None):
        return self._repository.whole_update(id, schema)

    def delete_by_id(self, id: str | ObjectId):
        return self._repository.delete_by_id(id)
