from app.repository.house_repository import HouseRepository
from app.services.base_service import BaseService


class HouseService(BaseService):
    def __init__(self):
        super().__init__(HouseRepository)
