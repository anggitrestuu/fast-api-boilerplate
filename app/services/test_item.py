from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.test_item import TestItemRepository
from app.models.test_item import TestItem
from app.schemas.test_item import TestItemCreate, TestItemUpdate
from app.core.exceptions import APIError

class TestItemService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repository = TestItemRepository(TestItem, db)

    async def create(self, schema: TestItemCreate):
        return await self.repository.create(schema)

    async def get(self, id: int):
        item = await self.repository.get(id)
        if not item:
            raise APIError(f"Test item with id {id} not found", status_code=404)
        return item

    async def get_multi(self, skip: int = 0, limit: int = 10, filters: dict = None):
        return await self.repository.get_multi(skip=skip, limit=limit, filters=filters)

    async def update(self, id: int, schema: TestItemUpdate):
        item = await self.repository.update(id=id, schema=schema)
        if not item:
            raise APIError(f"Test item with id {id} not found", status_code=404)
        return item

    async def delete(self, id: int):
        if not await self.repository.delete(id=id):
            raise APIError(f"Test item with id {id} not found", status_code=404)
        return True