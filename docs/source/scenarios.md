# Scenarios

With ARMA you can create scenarios by adding your own uses cases to OpenAPI paths.



:::{card} a_real_settings.json

```json
{
  "update_on_start": true,
  "mock_api_from_json_file": true,
  "functions_to_endpoints": {
    "/api/v1/test/create": "ScenarioCheckBodyVariableValue",
    "/api/v1/simple": "SimpleFunction"
  }
}
```
:::

Update the file:
- functions_to_endpoints/main.py


```python
from fastapi import Request
from fastapi.responses import JSONResponse
from jsf import JSF


class SimpleFunction:

    @classmethod
    async def response(cls, request: Request, url_data: dict):

        return JSONResponse("from SimpleFunction", status_code=201)
```
:::{card} SimpleFunction
The SimpleFunction class is straightforward:

Its response method takes a Request object and a url_data dictionary as input.<p>
It returns a JSON response with the message "from SimpleFunction" and a status code of 201.

:::

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from jsf import JSF

class ScenarioCheckBodyVariableValue:

    @classmethod
    async def response(cls, request: Request, url_data: dict):
        payload = await request.json()

        if payload["payload_id"] == "123":
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
```
:::{card} ScenarioCheckBodyVariableValue
The ScenarioCheckBodyVariableValue class is more complex:

Its response method also takes a Request object and a url_data dictionary.<p>
It retrieves the JSON payload from the request body using await request.json().<p>
It checks the value of payload["payload_id"]:<p>
If it's "123", it uses the jsf library to generate fake data based on the schema specified in url_data['responses']["200"]['schema'] and returns a JSON response with the generated data and a status code of 200.<p>
If it's not "123", it generates fake data based on the schema in url_data['responses']["405"]['schema'] and returns a JSON response with the generated data and a status code of 405.
:::
::: {card} {bdg-primary}`url_data` {bdg-primary-line}`schema`
```json
{
{}
}
```
:::