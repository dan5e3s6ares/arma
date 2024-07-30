import logging
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from middleware.exceptions import (
    MethodNotAllowed,
    NotFoundError,
    ValidationErrorException,
)

from .schemas import ErrorsModel, HeadersResponseModel

app = FastAPI()


async def default_json_response(
    content_type: str,
    content_errors: Any,
    status_code: int = 404,
    headers: HeadersResponseModel = HeadersResponseModel(),
    content_title: str = "Invalid Request",
):
    return JSONResponse(
        status_code=status_code,
        headers={"content-type": headers.content_type},
        content=ErrorsModel(
            **{
                "type": content_type,
                "title": content_title,
                "errors": content_errors,
            }
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return await default_json_response(
        content_type="ValidationError",
        content_errors=exc.errors(),
        status_code=422,
    )


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ValidationError as exc:
            return await default_json_response(
                content_type="ValidationError",
                content_errors=exc.errors(),
                status_code=422,
            )
        except ValueError as exc:
            return await default_json_response(
                content_type="ValueError",
                content_errors=exc.args[0],
                status_code=400,
            )
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={
                    "error": "client Error",
                    "message": str(http_exception.detail),
                },
            )
        except NotFoundError as exc:
            return await default_json_response(
                content_type="NotFound",
                content_errors=exc.errors(),
                status_code=400,
            )
        except ValidationErrorException as exc:
            return await default_json_response(
                content_type="ValidationError",
                content_errors=exc.errors(),
                status_code=422,
            )
        except MethodNotAllowed as exc:
            return await default_json_response(
                content_type="MethodNotAllowed",
                content_errors=exc.errors(),
                status_code=405,
            )
        except Exception as e:
            _id = str(uuid4())
            logging.critical("ID: %s | Message : %s", _id, str(e))
            message = (
                f"Please contact your service provider and inform the"
                f"id: {_id}"
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": "There was a problem processing your request",
                    "message": message,
                },
            )
