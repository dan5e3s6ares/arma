# Create your Classes here

from fastapi import Request
from fastapi.responses import JSONResponse


class TestClass:

    @classmethod
    def response(cls, request: Request, url_data: dict):

        return JSONResponse("from TestClass", status_code=201)
