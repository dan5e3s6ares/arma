<p align="center">
    <em>ARMA, high performance, easy to learn, fast to code, ready for production</em>
</p>
# A Real Mock API

ARMA is a set of packages for API mocking and contract testing with **OpenAPI v3.x**.

ARMA provides:

- **Mock Servers**: Life-like mock servers from any API specification document.
- **Validation Proxy**: Contract Testing for API consumers and developers.
- **Comprehensive API Specification Support**: OpenAPI v3.1, OpenAPI v3.0.

## Ways to Use ARMA

### Self-hosted ARMA

ARMA is an open-source HTTP server run from the command-line. It provides mocking, request validation, and content negotiation. Use it standalone tool or in continuous integration.

### Start Self-hosted ARMA

ARMA requires

- Docker-Compose >= 2.29.1

```bash
docker compose up --build
```

### Mocking

ARMA can help you create a fake "mock" based off an OpenAPI document, which helps people see how your API will work before you even have it built. Run it locally with the HTTP server.

Update the file:
- a_real_settings.json

Add one of the following keys to mock from URL:

| Key     | Type   | Description    |
| :---:   | :---: | :---: |
| mock_api_swaggerUrl   | string | Mock an API from Json Swagger URL |
| mock_api_swaggerYamlUrl | string   | Mock an API from Yaml Swagger URL   |
| update_on_start | boolean | True to update allways after restart the container |
| update_time_interval | integer | Feature not ready
** HINT - For the first run, you need to set ```"update_on_start": true```

Add one of the following keys to mock from file:

| Key     | Type   | Description    |
| :---:   | :---: | :---: |
| mock_api_from_json_file   | boolean | Mock an API from Json Swagger FILE |
| mock_api_from_yaml_file | boolean   | Mock an API from Yaml Swagger FILE   |
* save the file in the folder ```files``` with the name ```openapi.json or openapi.yaml```

### Scenarios

With ARMA you can create scenarios by adding your own uses cases to OpenAPI paths.

Update the file:
- functions_to_endpoints/main.py

Add one of the following keys to a_real_settings file:

| Key     | Type   | Description    |
| :---:   | :---: | :---: |
| <path_url>   | string | The url key from paths and your Class Name|

Example Function:

```python
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


### 🏁 Help Others Utilize ARMA

If you're using ARMA for an interesting use case, [contact us](mailto:daniel@soaresmartins.com) for a case study. We'll add it to a list here. Spread the goodness 🎉

### 👏 Contributing

If you are interested in contributing to ARMA itself, check out our [contributing docs ⇗][contributing] and [code of conduct ⇗][code_of_conduct] to get started.

### 🎉 Thanks

ARMA is built on top of lots of excellent packages, and here are a few we'd like to say a special thanks to.

- [rocketry](https://rocketry.readthedocs.io/en/stable/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
- [jsf](https://github.com/ghandic/jsf)
- [ruamel-yaml](https://yaml.readthedocs.io/en/latest/)
- [fastapi](https://fastapi.tiangolo.com/)

Check these projects out!

### 🌲 Sponsor ARMA by Planting a Tree

If you would like to thank us for creating ARMA, we ask that you [**buy the world a tree**](https://ecologi.com/stoplightinc).

[code_of_conduct]: CODE_OF_CONDUCT.md
[contributing]: CONTRIBUTING.md
[download-release]: https://github.com/stoplightio/prism/releases/latest
