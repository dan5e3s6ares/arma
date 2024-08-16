import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app

DEFAULT_HEADERS = {"header1": "value1", "header2": "value2"}


def form_mock():
    return {
        "PARAMETERS": {"headers_param": {"required": ["header1"]}},
        "POST": {
            "200": {},
            "payload": {
                "schema": {
                    "properties": {"abc": {"type": "string"}},
                    "type": "object",
                },
            },
            "queries_param": {"required": []},
            "headers_param": {"required": ["header1"]},
            "responses": {
                "200": {
                    "schema": {
                        "type": "object",
                        "properties": {"author": {"type": "string"}},
                        "required": ["author"],
                    },
                }
            },
        },
    }, "/url"


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_hello(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Healthy")

    @patch("functions.url_handle.BuildUrlDict.get_path_dict")
    def test_url_not_found(self, mock):
        mock.return_value = {"v2": "abc"}

        response = self.client.post(
            "/wrong/url",
            headers=DEFAULT_HEADERS,
            data={"abc": "abc"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            {
                'type': 'NotFound',
                'title': 'Invalid Request',
                'errors': [
                    {
                        'detail': 'Url Not Found',
                        'pointer': ['path', 'wrong/url'],
                    }
                ],
            },
            response.json(),
        )

    @patch("app.api.UrlHandler.find_matching_url")
    def test_payload_validation_and_response(self, mock):
        mock.return_value = form_mock()

        response = self.client.post(
            "/url/test-path?param1=value1&param2=value2",
            headers=DEFAULT_HEADERS,
            data={"abc": "abc"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("author", response.json(), "Key Not Found")

    @patch("app.api.UrlHandler.find_matching_url")
    def test_method_not_allowed(self, mock):
        response, path = form_mock()

        response["GET"] = response.pop("POST")

        mock.return_value = response, path

        response = self.client.post(
            "/url/test-path?param1=value1&param2=value2",
            headers=DEFAULT_HEADERS,
            data={"abc": "abc"},
        )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            {
                'type': 'MethodNotAllowed',
                'title': 'Invalid Request',
                'errors': [
                    {'detail': 'Method not allowed', 'pointer': ['POST']}
                ],
            },
            response.json(),
        )

    @patch("app.api.UrlHandler.find_matching_url")
    def test_headers(self, mock):
        response, path = form_mock()

        mock.return_value = response, path

        response = self.client.post(
            "/url/test-path?param1=value1&param2=value2",
            headers={"header2": "value2"},
            data={"abc": "abc"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {
                'type': 'ValidationError',
                'title': 'Invalid Request',
                'errors': [
                    {'detail': 'Missing Field', 'pointer': [0, 'header1']}
                ],
            },
        )

        response, path = form_mock()
        response.pop("PARAMETERS")
        mock.return_value = response, path

        response = self.client.post(
            "/url/test-path?param1=value1&param2=value2",
            headers={"header2": "value2"},
            data={"abc": "abc"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {
                'type': 'ValidationError',
                'title': 'Invalid Request',
                'errors': [
                    {'detail': 'Missing Field', 'pointer': [0, 'header1']}
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
