from app.repository.house_repository import HouseRepository
from app.services.base_service import BaseService


class HouseService(BaseService):
    def __init__(self):
        house_repository = HouseRepository()
        super().__init__(house_repository)
