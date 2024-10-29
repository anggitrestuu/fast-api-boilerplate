from fastapi import APIRouter
from app.api.v1.endpoints import example

api_router = APIRouter()

# Include your endpoint routers here
api_router.include_router(example.router, prefix="/example", tags=["example"])
# api_router.include_router(route1.router, prefix="/route1", tags=["route1"])
# api_router.include_router(route2.router, prefix="/route2", tags=["route2"])