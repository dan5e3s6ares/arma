from pydoc import locate

from fastapi import Request
from fastapi.responses import JSONResponse
from jsf import JSF


class FunctionsToEndpoints:
    data = {}

    @classmethod
    def set_data(cls, data: dict):
        cls.data = data

    @classmethod
    async def build_response(
        cls, path: str, request: Request, from_function: dict
    ):
        try:
            my_class = locate(
                "functions_to_endpoints.main."
                + cls.data["functions_to_endpoints"]["/" + path]
            )
            return await my_class.response(
                request=request, url_data=from_function
            )
        except KeyError:
            payload = await request.body()
            fake_json = {}

            if payload != {}:
                fake_json = payload

            key = 200
            for item in from_function['responses'].items():
                faker = JSF(from_function['responses'][item[0]]["schema"])
                fake_json = faker.generate(
                    n=1, use_defaults=True, use_examples=True
                )
                key = item[0]
                break
            return JSONResponse(fake_json, status_code=int(key))
