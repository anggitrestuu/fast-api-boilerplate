# app/api/v1/endpoints/test_items.py
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.test_item import TestItemService
from app.schemas.test_item import TestItemInDB, TestItemCreate, TestItemUpdate
from app.utils.response_handler import response

router = APIRouter()

@router.post("/", response_model=TestItemInDB)
async def create_item(
    schema: TestItemCreate,
    service: TestItemService = Depends()
):
    item = await service.create(schema)
    return response.success(
        data=TestItemInDB.model_validate(item),
        message="Test item created successfully"
    )

@router.get("/", response_model=list[TestItemInDB])
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[bool] = None,
    service: TestItemService = Depends()
):
    items, total = await service.get_multi(skip=skip, limit=limit, filters={"status": status})
    
    return response.success(
        data=[TestItemInDB.model_validate(item) for item in items],
        message="Test items retrieved successfully",
        meta={
            "page": skip // limit + 1,
            "per_page": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    )

@router.get("/{id}", response_model=TestItemInDB)
async def get_item(
    id: int,
    service: TestItemService = Depends()
):
    item = await service.get(id)
    return response.success(
        data=TestItemInDB.model_validate(item),
        message="Test item retrieved successfully"
    )

@router.put("/{id}", response_model=TestItemInDB)
async def update_item(
    id: int,
    schema: TestItemUpdate,
    service: TestItemService = Depends()
):
    item = await service.update(id, schema)
    return response.success(
        data=TestItemInDB.model_validate(item),
        message="Test item updated successfully"
    )

@router.delete("/{id}")
async def delete_item(
    id: int,
    service: TestItemService = Depends()
):
    await service.delete(id)
    return response.success(message="Test item deleted successfully")