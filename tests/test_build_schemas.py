import unittest

from fastapi.testclient import TestClient

from app.api import app
from functions.schemas_service import SchemaServices


class TestSchemas(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.fixtures = {
            "content": {
                "*/*": {
                    "schema": {
                        "description": "Podcast model",
                        "properties": {
                            "author": {"type": "string"},
                            "block": {"type": "boolean"},
                            "categories": {
                                "items": {"type": "string"},
                                "type": "array",
                                "uniqueItems": True,
                            },
                            "copyright": {"type": "string"},
                            "country": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["categories", "description"],
                        "type": "object",
                    },
                    "description": "OK",
                }
            },
            "tags": ["API-v2"],
        }

    def test_build(self):
        response = SchemaServices.build(self.fixtures)
        assert response == {
            'content_type': '*/*',
            'schema': {
                'description': 'Podcast model',
                'properties': {
                    'author': {'type': 'string'},
                    'block': {'type': 'boolean'},
                    'categories': {
                        'items': {'type': 'string'},
                        'type': 'array',
                        'uniqueItems': True,
                    },
                    'copyright': {'type': 'string'},
                    'country': {'type': 'string'},
                    'description': {'type': 'string'},
                },
                'required': ['categories', 'description'],
                'type': 'object',
            },
        }
