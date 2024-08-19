# Mocking
ARMA can help you create a fake "mock" based off an OpenAPI document, which helps people see how your API will work before you even have it built. Run it locally with the HTTP server.
The a_real_settings.json file serves as the central repository for all ARMA configuration data.
:::{card} a_real_settings.json
```json
{
  "mock_api_swaggerUrl": "https//www.yourapi.com/doc/swagger.json",
  "mock_api_swaggerYamlUrl": "https//www.yourapi.com/doc/swagger.ymal",
  "update_on_start": true,
  "mock_api_from_json_file": true,
  "mock_api_from_yaml_file": true,
  "functions_to_endpoints": {
    "/api/v1/test/create": "TestClass"
  }
}

```
:::

:::{card} mock_api_swaggerUrl ```string```
- The endpoint of the Swagger JSON file for the API you intend to mock
:::
:::{card} mock_api_swaggerYamlUrl ```string```
- The endpoint of the Swagger YAML file for the API you intend to mock
:::
:::{card} update_on_start ```boolean```
- To enable automatic server updates based on the Swagger file's configuration, set this option to 'true'.
:::
:::{card} update_time_interval ```integer```
- This feature is currently under development and is not yet available.
:::
:::{card} mock_api_from_json_file ```boolean```
- Initiates the server, leveraging the openapi.json file within the 'files' directory as a foundation. This action precedes the execution of the mock_api_from_yaml_file function.
:::
:::{card} mock_api_from_yaml_file ```boolean```
- Starts the server using the openapi.yaml file located in the 'files' folder as a base. This function is blocked by the mock_api_from_json_file function.
:::
:::{card} functions_to_endpoints ```object```
- Starts Indicates the particular Swagger documentation endpoint that will trigger your personalized function to be executed.
    :::{card} key ```string```
        Key value from openapi 'paths'
    :::

    :::{card} value ```string```
        Your personalized Class name logic for processing.
    :::
:::

** HINT - For the first run, you need to set ```"update_on_start": true```