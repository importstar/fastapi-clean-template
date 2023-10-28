from app.models import House
from app.repository.base_repository import BaseRepository


class HouseRepository(BaseRepository):
    def __init__(self):
        super().__init__(House)
