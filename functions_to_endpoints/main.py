from fastapi import Request
from fastapi.responses import JSONResponse
from jsf import JSF


class SimpleFunction:

    @classmethod
    async def response(cls, request: Request, url_data: dict):

        return JSONResponse("from SimpleFunction", status_code=201)


class CheckBodyVariableValue:

    @classmethod
    async def response(cls, request: Request, url_data: dict):
        payload = await request.json()

        if payload.payload_id == "123":
            faker = JSF(url_data['responses']["200"]['schema'])
            fake_payload_response = faker.generate(
                n=1, use_defaults=True, use_examples=True
            )
            return JSONResponse(fake_payload_response, status_code=200)
        else:
            faker = JSF(url_data['responses']["405"]['schema'])
            fake_payload_response = faker.generate(
                n=1, use_defaults=True, use_examples=True
            )
            return JSONResponse(fake_payload_response, status_code=405)
