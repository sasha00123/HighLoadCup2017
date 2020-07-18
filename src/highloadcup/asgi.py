from fastapi.exceptions import RequestValidationError, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from .main import get_app

app = get_app()


@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
    )
