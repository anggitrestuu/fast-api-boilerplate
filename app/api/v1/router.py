from fastapi import APIRouter
from app.api.v1.endpoints import example, test_items

api_router = APIRouter()

# Include your endpoint routers here
api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(test_items.router, prefix="/test-items", tags=["test-items"])