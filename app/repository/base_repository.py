import datetime
import re

from pydantic import BaseModel

from bson import ObjectId

from typing import Any

from mongoengine import Document, QuerySet, errors

from app.core.exceptions import DuplicatedError, NotFoundError, ValidationError


class BaseRepository:
    def __init__(self, model: Document):
        self.model = model

    def get_by_options(
        self, schema: BaseModel | None = None, **kwargs: str
    ) -> QuerySet:
        items = self.model.objects(
            **{**(schema.model_dump(exclude_defaults=True) if schema else {}), **kwargs}
        )
        if not items:
            raise NotFoundError(detail="not found")

        return items

    def get_by_id(self, id: str | ObjectId) -> Document:
        if not ObjectId.is_valid(id):
            raise ValidationError("Invalid ObjectId")

        try:
            item = self.model.objects.with_id(id)
        except errors.ValidationError as e:
            raise ValidationError(detail=str(e))

        if not item:
            raise NotFoundError(detail=f"ObjectId('{str(id)}') not found")

        return item

    def create(self, schema: None | BaseModel = None, **kwargs: int) -> Document:
        item = self.model(
            **{
                **(schema.model_dump(exclude_defaults=True) if schema else {}),
                **kwargs,
            }
        )
        try:
            item.save()
        except errors.NotUniqueError as e:
            duplicate = re.search("'keyValue': {.*?}", str(e)).group(0)
            duplicate = re.search("{.*?}", duplicate).group(0)
            raise DuplicatedError(detail=f"'DuplicateError': {duplicate}")

        except Exception as e:
            raise ValidationError(detail=str(e))

        return self.get_by_id(item.id)

    def update(
        self, id: str | ObjectId, schema: BaseModel | None = None, **kwargs: int
    ) -> Document:
        item = self.get_by_id(id)
        try:
            item.update(
                **{
                    **(schema.model_dump(exclude_defaults=True) if schema else {}),
                    **kwargs,
                }
            )
        except Exception as e:
            raise ValidationError(detail=str(e))

        return self.get_by_id(id)

    def update_attr(self, id: str | ObjectId, attr: str, value: Any) -> Document:
        item = self.get_by_id(id)
        try:
            item.update(**{attr: value})
        except Exception as e:
            raise ValidationError(detail=str(e))

        return self.get_by_id(id)

    def whole_update(
        self, id: str | ObjectId, schema: BaseModel | None = None, **kwargs: int
    ) -> Document:
        item = self.get_by_id(id)
        try:
            item.update(
                **{
                    **(schema.model_dump(exclude_defaults=True) if schema else {}),
                    **kwargs,
                }
            )
        except Exception as e:
            raise ValidationError(detail=str(e))

        return self.get_by_id(id)

    def delete_by_id(self, id: str | ObjectId) -> Document:
        item = self.get_by_id(id)
        try:
            item.delete()
        except Exception as e:
            raise ValidationError(detail=str(e))

        return item
