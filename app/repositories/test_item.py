from app.core.repository import BaseRepository
from app.models.test_item import TestItem
from app.schemas.test_item import TestItemCreate, TestItemUpdate

class TestItemRepository(BaseRepository[TestItem, TestItemCreate, TestItemUpdate]):
    pass