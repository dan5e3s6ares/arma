import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app
from functions.read_settings import ReadSettingsFile
from functions.url_handle import UrlHandler
from tests.fixtures import open_api_mock, settings_mock


class TestSchemas(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("functions.read_settings.ReadSettingsFile.read_file")
    @patch("functions.url_handle.BuildUrlDict.read_file")
    async def test_read(self, mock_read_file, mock_open_api):
        mock_read_file.return_value = open_api_mock()
        mock_open_api.return_value = settings_mock()
        await ReadSettingsFile.read()
        _, path, _ = await UrlHandler.find_matching_url(
            "/api/v2/podcasts/create"
        )
        self.assertEqual("/" + path, list(open_api_mock()["paths"].keys())[0])
