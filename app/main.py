from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.exceptions import (
    APIError,
    api_error_handler,
    validation_error_handler,
    sqlalchemy_error_handler
)
from app.api.v1.router import api_router
from app.utils.response_handler import success_response

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add exception handlers
    application.add_exception_handler(APIError, api_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)
    application.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)

    # Add routers
    application.include_router(api_router, prefix=settings.API_V1_STR)

    @application.get("/health")
    async def health_check():
        return success_response(
            data={"status": "healthy"},
            message="Service is healthy"
        )

    return application

app = create_application()