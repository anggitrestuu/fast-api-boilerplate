from typing import Any, Optional
from fastapi.responses import JSONResponse
from app.schemas.response import StandardResponse, Meta, Error

def success_response(
    data: Any = None,
    message: str = "Success",
    meta: Optional[Meta] = None,
    status_code: int = 200
) -> JSONResponse:
    response = StandardResponse(
        success=True,
        message=message,
        data=data,
        meta=meta,
        errors=None
    )
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(exclude_none=True)
    )

def error_response(
    message: str = "Error",
    errors: Optional[list[Error]] = None,
    status_code: int = 400
) -> JSONResponse:
    response = StandardResponse(
        success=False,
        message=message,
        data=None,
        meta=None,
        errors=errors
    )
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(exclude_none=True)
    )