import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from functions.endpoints_functions import FunctionsToEndpoints
from functions.query_params import CheckParams
from functions.read_settings import ReadSettingsFile
from functions.syncronize import scheduler
from functions.url_handle import UrlHandler
from middleware.exceptions import (
    MethodNotAllowed,
    NotFoundError,
    ValidationErrorException,
)
from middleware.handler import (
    ExceptionHandlerMiddleware,
    validation_exception_handler,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ReadSettingsFile.read()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.add_middleware(ExceptionHandlerMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.route("/healthcheck", methods=["GET"])
async def hello(request: Request):
    return JSONResponse("Healthy")


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def catch_all(request: Request, path_name: str):

    try:
        from_function, path, path_params = await UrlHandler.find_matching_url(
            path_name
        )
    except KeyError as e:
        raise NotFoundError(
            [{"msg": "Url Not Found", "loc": ["path", path_name]}]
        ) from e

    try:
        full_path = from_function
        from_function = from_function[request.method]
    except KeyError as e:
        raise MethodNotAllowed(
            [{"msg": "Method not allowed", "loc": [request.method]}]
        ) from e

    keys = list(from_function.keys())
    if "queries_param" in keys:
        await CheckParams.headers_query_params(
            rules_dict=from_function["queries_param"],
            params_dict=await CheckParams.transfrom_query_params(
                request.url.query
            ),
            position="query-params",
        )

    if "path_params" in keys:
        await CheckParams.headers_query_params(
            rules_dict=from_function["path_params"],
            params_dict=path_params,
            position="path-params",
        )

    if "PARAMETERS" in full_path:
        await CheckParams.headers_query_params(
            rules_dict=full_path["PARAMETERS"]["headers_param"],
            params_dict=dict(request.headers),
            position="headers",
        )

    if "headers_param" in keys:
        await CheckParams.headers_query_params(
            rules_dict=from_function["headers_param"],
            params_dict=dict(request.headers),
            position="headers",
        )

    try:
        payload = await request.json()
    except json.decoder.JSONDecodeError:
        payload = {}

    try:
        required = False
        if from_function.get("payload", None):
            required = from_function["payload"].get("required", None)
            validate(
                instance=payload,
                schema=from_function["payload"]["schema"],
            )

        if required and payload == {}:
            raise MethodNotAllowed(
                [{"msg": "Payload required", "loc": [request.method]}]
            )
    except ValidationError as e:
        errors = [
            {
                "detail": e.message,
                "pointer": [e.json_path],
            }
        ]
        raise ValidationErrorException(errors) from e
    except KeyError as e:
        raise MethodNotAllowed(
            [{"msg": "Payload not allowed", "loc": [request.method]}]
        ) from e

    return await FunctionsToEndpoints.build_response(
        path=path, request=request, from_function=from_function
    )
