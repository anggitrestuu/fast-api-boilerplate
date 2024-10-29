from typing import Optional
from fastapi import APIRouter, Depends
from app.services.test_item import TestItemService
from app.schemas.test_item import TestItem, TestItemCreate, TestItemUpdate
from app.utils.pagination import PaginationParams
from app.utils.response_handler import success_response

router = APIRouter()

@router.post("/", response_model=TestItem)
async def create_item(
    item_in: TestItemCreate,
    service: TestItemService = Depends()
):
    item = service.create_item(item_in)
    return success_response(
        data=item,
        message="Item created successfully"
    )

@router.get("/{item_id}", response_model=TestItem)
async def get_item(
    item_id: int,
    service: TestItemService = Depends()
):
    item = service.get_item(item_id)
    return success_response(
        data=item,
        message="Item retrieved successfully"
    )

@router.get("/")
async def get_items(
    pagination: PaginationParams = Depends(),
    service: TestItemService = Depends()
):
    result = service.get_items(pagination)
    return success_response(
        data=result.items,
        message="Items retrieved successfully",
        meta={
            "page": result.page,
            "per_page": result.page_size,
            "total": result.total,
            "total_pages": result.total_pages
        }
    )

@router.put("/{item_id}", response_model=TestItem)
async def update_item(
    item_id: int,
    item_in: TestItemUpdate,
    service: TestItemService = Depends()
):
    item = service.update_item(item_id, item_in)
    return success_response(
        data=item,
        message="Item updated successfully"
    )

@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    service: TestItemService = Depends()
):
    service.delete_item(item_id)
    return success_response(
        message="Item deleted successfully"
    )