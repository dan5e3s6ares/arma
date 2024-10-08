import json
import logging
from typing import List

from fastapi import BackgroundTasks

from functions.schemas_service import SchemaServices

logger = logging.getLogger(__name__)


tasks = BackgroundTasks()


class BuildUrlDict:
    components = {}
    path_dict = {}
    path_queries = {}
    path_headers = {}
    path_payload = {}

    @classmethod
    def get_path_dict(cls):
        return cls.path_dict

    @classmethod
    def get_path_queries(cls):
        return cls.path_queries

    @classmethod
    def get_path_headers(cls):
        return cls.path_headers

    @classmethod
    def read_file(cls):
        data = None
        with open("files/openapi.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    @classmethod
    def sync(cls):
        cls.components = cls.read_file()
        cls.list_to_hierarchy_dict(cls.components['paths'])
        print("Paths Synced")

    @classmethod
    def check_if_regex(cls, schema: dict):
        if schema:
            if (
                schema.get("type", None) == "integer"
                and schema.get("format", None) == "int64"
            ):
                schema['type'] = "string"
                schema['pattern'] = "^-?(0|[1-9]\\d{0,18})$"
            elif (
                schema.get("type", None) == "integer"
                and schema.get("format", None) == "int32"
            ):
                schema['type'] = "string"
                schema['pattern'] = "^-?(0|[1-9]\\d{0,9})$"
            elif (
                schema.get("type", None) == "number"
                and schema.get("format", None) == "float"
            ):
                schema['type'] = "string"
                schema['pattern'] = "^-?(0|[1-9]\\d{0,9})(\\.\\d{1,6})?$"
            elif schema.get("format", None) == "uuid":
                schema['pattern'] = (
                    "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
                )
            elif schema.get("type", None) == "boolean":
                schema['type'] = "string"
                schema['pattern'] = "^(true|false)$"
        return schema

    @classmethod
    def _classify_parameters(cls, parameter: dict, parameters_queries: dict):
        if parameter.get("required", False):
            parameters_queries["required"].append(parameter["name"])
        parameters_queries["additionalProperties"] = parameter.get(
            "additionalProperties", False
        )
        parameters_queries["optional"].append(parameter["name"])
        parameters_queries['properties'][parameter["name"]] = (
            cls.check_if_regex(parameter.get("schema", None))
        )
        return parameters_queries

    @classmethod
    def build_query_params(cls, parameters: List):
        path_queries = {
            "required": [],
            "optional": [],
            "properties": {},
            "type": "object",
        }
        path_headers = {
            "required": [],
            "optional": [],
            "properties": {},
            "type": "object",
        }
        path_params = {
            "required": [],
            "optional": [],
            "properties": {},
            "type": "object",
        }
        for parameter in parameters:
            if "$ref" not in parameter.keys() and parameter["in"] == "query":
                path_queries = cls._classify_parameters(
                    parameter, path_queries
                )
            elif (
                "$ref" not in parameter.keys() and parameter["in"] == "header"
            ):
                path_headers = cls._classify_parameters(
                    parameter, path_headers
                )
            elif "$ref" not in parameter.keys() and parameter["in"] == "path":
                path_params = cls._classify_parameters(parameter, path_params)
            elif "$ref" in parameter.keys():
                ref = parameter["$ref"].split("/")[1:]
                actual = cls.components
                for item in ref:
                    actual = actual[item]
                if actual["in"] == "query":
                    path_queries = cls._classify_parameters(
                        actual, path_queries
                    )
                elif actual["in"] == "header":
                    path_headers = cls._classify_parameters(
                        actual, path_headers
                    )
                elif actual["in"] == "path":
                    path_params = cls._classify_parameters(actual, path_params)
        cls.path_headers = path_headers
        cls.path_headers["additionalProperties"] = True
        return {
            "queries_param": path_queries,
            "headers_param": path_headers,
            "path_params": path_params,
        }

    @classmethod
    def build_path_params(cls, data: dict):
        response = {
            "queries_param": {
                "required": [],
                "optional": [],
                "properties": {},
                "type": "object",
            },
            "headers_param": {
                "required": [],
                "optional": [],
                "properties": {},
                "type": "object",
                "additionalProperties": True,
            },
            "path_params": {
                "required": [],
                "optional": [],
                "properties": {},
                "type": "object",
            },
        }
        try:
            if "parameters" in data:
                response = cls.build_query_params(data["parameters"])
            SchemaServices.load_components(cls.components)
            response['responses'] = {}
            for item in data['responses'].items():
                response['responses'][item[0]] = SchemaServices.build(item[1])
            response['payload'] = SchemaServices.build(data["requestBody"])
        except KeyError:
            pass
        except TypeError:
            response = cls.build_query_params(data)
        return response

    @classmethod
    def build_actions(cls, path: str, actions: dict):
        cls.path_queries[path] = {}
        for item in actions.items():
            key = item[0].upper()
            cls.path_queries[path][key] = cls.build_path_params(item[1])

    @classmethod
    def list_to_hierarchy_dict(cls, url_patterns: dict):
        url_patterns_list = []

        for pattern in url_patterns.items():

            cls.build_actions(pattern[0], pattern[1])

            pattern_parts = pattern[0].split("/")
            if pattern_parts[0] == "":
                del pattern_parts[0]
            url_patterns_list.append(pattern_parts)

        cls._build_dict(url_patterns_list)

    @classmethod
    def _build_dict(cls, url_patterns: List):
        result = {}
        for path in url_patterns:
            current_dict = result
            for element in path:
                if element not in current_dict:
                    current_dict[element] = {}
                current_dict = current_dict[element]
        cls.path_dict = result


class UrlHandler:

    @classmethod
    def sync(cls) -> None:
        tasks.add_task(BuildUrlDict.sync())

    @classmethod
    async def find_matching_url(cls, url_param: str):

        url_parts = url_param.split("/")
        if url_parts[0] == "":
            del url_parts[0]

        path = ""
        initial_path = BuildUrlDict.get_path_dict()
        keys_values = {}

        for item in url_parts:
            try:
                _ = initial_path[item]
                if path == "":
                    path = item
                else:
                    path = path + "/" + item
                initial_path = initial_path[item]
            except KeyError:
                for key in initial_path.items():
                    if "{" in key[0]:
                        keys_values[key[0][1:-1]] = item
                        path = path + "/" + key[0]
                        initial_path = initial_path[key[0]]
                        break
        return BuildUrlDict.get_path_queries()["/" + path], path, keys_values
