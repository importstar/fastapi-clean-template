from mongoengine import connect, disconnect_all, DEFAULT_CONNECTION_NAME, Document
from mongoengine.base.common import _get_documents_by_db

from loguru import logger

from app.models.house_model import House


async def init_mongoengine(settings) -> None:
    host = (
        settings.DATABASE_URI_FORMAT
        if settings.DB_USER and settings.DB_PASSWORD
        else "{db_engine}://{host}:{port}/{database}"
    ).format(
        db_engine=settings.DB_ENGINE,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
    logger.info("DB URI: " + host)
    connect(host=host, uuidRepresentation="standard")
    logger.info("Initialized mongengine")


async def disconnect_mongoengine() -> None:
    disconnect_all()
    logger.info("Closed all mongoengine connections")


cls_documents: list[Document] = _get_documents_by_db(
    DEFAULT_CONNECTION_NAME, DEFAULT_CONNECTION_NAME
)
