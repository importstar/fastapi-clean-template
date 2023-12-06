from fastapi import Query

from fastapi_pagination import default

from app.core.config import settings

Page = default.Page.with_custom_options(
    size=Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
)
"""If doesn't need a custom pagination

Just use `Page` from `from fastapi_pagination import Page` instead."""
