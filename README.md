# a-real-mock-api
A real server to mock any api , really easy to use

{
  "mock_api_swaggerUrl": "https://api.apis.guru/v2/specs/zeno.fm/0.6-99cfdac/openapi.json",
  "mock_api_swaggerYamlUrl": "",
  "mock_api_from_yaml_file": "",
  "mock_api_from_json_file": "",
  "functions_to_endpoints": [
    { "function": "get_by_tags", "endpoint": "/pet/findByTags" },
    { "function": "create", "endpoint": "/pet" },
    { "function": "update", "endpoint": "/pet/<int:id>" }
  ],
  "update_on_start": true,
  "update_time_interval": 86400,
  "yaml_folder": "Install the PyYAML package or the uvicorn[standard] optional"
}