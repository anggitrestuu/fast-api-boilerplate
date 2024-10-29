from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TestItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: bool = True

class TestItemCreate(TestItemBase):
    pass

class TestItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[bool] = None

class TestItemInDB(TestItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)