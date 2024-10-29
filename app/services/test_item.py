from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.test_item import TestItemRepository
from app.schemas.test_item import TestItemCreate, TestItemUpdate
from app.utils.pagination import PaginationParams
from app.core.exceptions import APIError

class TestItemService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = TestItemRepository(db)

    def create_item(self, item_in: TestItemCreate):
        return self.repository.create(item_in)

    def get_item(self, item_id: int):
        item = self.repository.get_by_id(item_id)
        if not item:
            raise APIError(
                message=f"Item with id {item_id} not found",
                status_code=404
            )
        return item

    def get_items(self, params: PaginationParams):
        return self.repository.get_all(params)

    def update_item(self, item_id: int, item_in: TestItemUpdate):
        item = self.repository.update(item_id, item_in)
        if not item:
            raise APIError(
                message=f"Item with id {item_id} not found",
                status_code=404
            )
        return item

    def delete_item(self, item_id: int):
        if not self.repository.delete(item_id):
            raise APIError(
                message=f"Item with id {item_id} not found",
                status_code=404
            )
        return True