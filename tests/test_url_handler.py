import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app
from functions.url_handle import BuildUrlDict
from tests.fixtures import open_api_mock

DEFAULT_HEADERS = {"header1": "value1", "header2": "value2"}


class TestUrlHandle(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("functions.url_handle.BuildUrlDict.read_file")
    def test_sync(self, mock):
        mock.return_value = open_api_mock()
        action = BuildUrlDict
        action.sync()
        self.assertEqual(
            list(action.get_path_queries().keys())[0],
            list(open_api_mock()['paths'].keys())[0],
        )
