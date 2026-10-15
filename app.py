"""FastAPI application entry point."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from routes.tags import router as tags_router
from utils.errors import AppError, NotFoundError, ValidationError

app = FastAPI()
app.include_router(tags_router)


@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    """Convert an AppError raised by a service into an HTTP error response.

    Args:
        request: The request that raised the error.
        exc: The error raised by the service layer.

    Returns:
        A JSON response with the error message: 400 for ValidationError,
        404 for NotFoundError, and 500 for any other AppError.
    """
    if isinstance(exc, ValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})
