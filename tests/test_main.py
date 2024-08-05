import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app


def form_mock():
    return {
        "PARAMETERS": {"headers_param": {"required": []}},
        "POST": {
            "200": {},
            "payload": {
                "schema": {
                    "properties": {"abc": {"type": "string"}},
                    "type": "object",
                },
            },
            "queries_param": {"required": []},
            "headers_param": {"required": []},
            "responses": {
                "200": {
                    "schema": {
                        "type": "object",
                        "properties": {"author": {"type": "string"}},
                        "required": ["author"],
                    }
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

    @patch("app.api.UrlHandler.find_matching_url")
    def test_payload_validation_and_response(self, mock):
        mock.return_value = form_mock()

        response = self.client.post(
            "/url/test-path?param1=value1&param2=value2",
            headers={"header1": "value1", "header2": "value2"},
            data={"abc": "abc"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("author", response.json(), "Key Not Found")

    @patch("app.api.UrlHandler.find_matching_url")
    def test_MethodNotAllowed(self, mock):
        response, path = form_mock()

        response["GET"] = response.pop("POST")

        mock.return_value = response, path

        response = self.client.post(
            "/url/test-path?param1=value1&param2=value2",
            headers={"header1": "value1", "header2": "value2"},
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


if __name__ == "__main__":
    unittest.main()
