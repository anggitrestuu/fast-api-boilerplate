from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.test_item import TestItem
from app.schemas.test_item import TestItemCreate, TestItemUpdate
from app.utils.pagination import PaginationParams, paginate_query

class TestItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item_in: TestItemCreate) -> TestItem:
        item = TestItem(**item_in.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_id(self, item_id: int) -> Optional[TestItem]:
        return self.db.query(TestItem).filter(TestItem.id == item_id).first()

    def get_all(self, params: PaginationParams):
        query = self.db.query(TestItem)
        return paginate_query(query, params)

    def update(self, item_id: int, item_in: TestItemUpdate) -> Optional[TestItem]:
        item = self.get_by_id(item_id)
        if not item:
            return None
        
        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int) -> bool:
        item = self.get_by_id(item_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True