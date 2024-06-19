from fastapi import FastAPI, Request

app = FastAPI()


@app.route("/hello")
async def hello():
    return {"hello": "world"}


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def catch_all(request: Request, path_name: str):

    return {
        "request_method": request.method,
        "path_name": path_name,
        "query_params": request.query_params,
        "headers": request.headers,
        "body": await request.body(),
    }
