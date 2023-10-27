from mongoengine import connection
from loguru import logger


async def init_mongoengine(settings):
    host = settings.DATABASE_URI
    get_connection = connection.connect(host=host)
    logger.debug("DB URI: " + host)

    return get_connection


async def disconnect_mongoengine():
    connection.disconnect_all()
    logger.debug("Closed all mongoengine connections")
