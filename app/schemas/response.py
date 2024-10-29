from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")

class Meta(BaseModel):
    page: Optional[int] = None
    per_page: Optional[int] = None
    total: Optional[int] = None
    total_pages: Optional[int] = None

class Error(BaseModel):
    code: str
    message: str
    field: Optional[str] = None

class StandardResponse(GenericModel, Generic[DataT]):
    success: bool
    message: str
    data: Optional[DataT] = None
    meta: Optional[Meta] = None
    errors: Optional[list[Error]] = None

    class Config:
        arbitrary_types_allowed = True