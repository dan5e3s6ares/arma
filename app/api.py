from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from functions.query_params import CheckParams
from functions.read_settings import ReadSettingsFile
from functions.syncronize import scheduler
from functions.url_handle import UrlHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("@SERVIDOR INICIANDO@")
    await ReadSettingsFile.read()
    yield
    scheduler.shutdown()
    print("#SERVIDOR TERMINANDO#")


app = FastAPI(lifespan=lifespan)


@app.route("/healthcheck", methods=["GET"])
async def hello(request: Request):
    return JSONResponse("Healthy")


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def catch_all(request: Request, path_name: str):

    from_function = await UrlHandler.find_matching_url(path_name)

    try:
        from_function = from_function[request.method]

        all_keys_present = await CheckParams.query_params(
            rules_dict=from_function["queries_param"], params_dict=request.query_params
        )
        if not all_keys_present:
            return JSONResponse("Bad request", status_code=400)

        all_keys_present = await CheckParams.header_params(
            rules_dict=from_function["headers_param"], params_dict=request.headers
        )
        if not all_keys_present:
            return JSONResponse("Bad request Headers", status_code=400)

    except KeyError:
        return JSONResponse("Method not allowed", status_code=405)

    return {
        "request_method": request.method,
        "path_name": path_name,
        "query_params": request.query_params,
        "headers": request.headers,
        "body": await request.body(),
        "from_function": from_function,
    }
