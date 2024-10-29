from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Shared properties
class TestItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

# Properties to receive on item creation
class TestItemCreate(TestItemBase):
    pass

# Properties to receive on item update
class TestItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None

# Properties to return to client
class TestItem(TestItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True