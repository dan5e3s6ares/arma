import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jsf import JSF
from jsonschema import validate
from jsonschema.exceptions import ValidationError

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

    try:
        from_function = await UrlHandler.find_matching_url(path_name)
    except KeyError:
        return JSONResponse("Url not found", status_code=400)

    print(from_function)

    try:
        full_path = from_function
        from_function = from_function[request.method]

        all_keys_present = await CheckParams.query_params(
            rules_dict=from_function["queries_param"],
            params_dict=request.query_params,
        )
        if not all_keys_present:
            return JSONResponse("Bad request", status_code=400)

        if "PARAMETERS" in full_path:
            all_keys_present = await CheckParams.header_params(
                rules_dict=full_path["PARAMETERS"]["headers_param"],
                params_dict=request.query_params,
            )
            if not all_keys_present:
                return JSONResponse("Bad request parameters", status_code=400)

        all_keys_present = await CheckParams.header_params(
            rules_dict=from_function["headers_param"],
            params_dict=request.headers,
        )
        if not all_keys_present:
            return JSONResponse("Bad request Headers", status_code=400)

        payload = {}

        try:
            payload = await request.json()
            validate(
                instance=payload,
                schema=from_function["payload"]["schema"],
            )
        except json.decoder.JSONDecodeError:
            pass
        except ValidationError as e:
            errors = [
                {
                    "detail": e.message,
                    "pointer": [e.json_path],
                }
            ]
            return JSONResponse(errors, status_code=422)
        except KeyError:
            return JSONResponse("Payload not allowed", status_code=405)

    except KeyError:
        return JSONResponse("Method not allowed", status_code=405)

    fake_json = {}

    if payload != {}:
        fake_json = payload

    key = 200
    for item in from_function['responses'].items():
        faker = JSF(from_function['responses'][item[0]]['schema'])
        fake_json = faker.generate(n=1, use_defaults=True, use_examples=True)
        key = item[0]
        break
    return JSONResponse(fake_json, status_code=int(key))
    # return fake_json

    # return {
    #     "fake_reponse": fake_json,
    #     "request_method": request.method,
    #     "path_name": path_name,
    #     "query_params": request.query_params,
    #     "headers": request.headers,
    #     "body": await request.body(),
    #     "from_function": full_path,
    # }
