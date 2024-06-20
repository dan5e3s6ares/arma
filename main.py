from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.route("/healthcheck", methods=["GET"])
async def hello(request: Request):
    return JSONResponse("Healthy")


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def catch_all(request: Request, path_name: str):

    return {
        "request_method": request.method,
        "path_name": path_name,
        "query_params": request.query_params,
        "headers": request.headers,
        "body": await request.body(),
    }
