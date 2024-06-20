import unittest

from fastapi.testclient import TestClient

from main import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_hello(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Healthy")

    def test_catch_all(self):

        response = self.client.post(
            "/test-path?param1=value1&param2=value2",
            headers={"header1": "value1", "header2": "value2"},
            data="test body",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "request_method": "POST",
                "path_name": "test-path",
                "query_params": {"param1": "value1", "param2": "value2"},
                "headers": {
                    "host": "testserver",
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate",
                    "connection": "keep-alive",
                    "user-agent": "testclient",
                    "header1": "value1",
                    "header2": "value2",
                    "content-length": "9",
                },
                "body": "test body",
            },
        )


if __name__ == "__main__":
    unittest.main()
