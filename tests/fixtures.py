def open_api_mock():
    return {
        "openapi": "3.0.1",
        "servers": [
            {
                "description": "Generated server url",
                "url": "https://api.zeno.fm",
            }
        ],
        "info": {
            "description": "Aggregators API",
            "title": "Aggregators API Service",
            "version": "0.6-99cfdac",
            "x-apisguru-categories": ["media"],
            "x-logo": {"url": "https://api.apis.guru/v2/cache/logo/"},
            "x-origin": [
                {
                    "format": "openapi",
                    "url": "https://api.zeno.fm/v3/api-docs",
                    "version": "3.0",
                }
            ],
            "x-providerName": "zeno.fm",
        },
        "security": [{"API_Key": []}],
        "paths": {
            "/api/v2/podcasts/create": {
                "post": {
                    "description": "Create podcast",
                    "operationId": "createPodcast",
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "properties": {
                                        "file_logo": {
                                            "format": "binary",
                                            "type": "string",
                                        },
                                        "podcast": {
                                            "$ref": "#/components/schemas/Podcast"
                                        },
                                    },
                                    "required": ["file_logo", "podcast"],
                                    "type": "object",
                                }
                            }
                        }
                    },
                    "parameters": [
                        {
                            "in": "header",
                            "name": "podcastKey",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "*/*": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Podcast"
                                    }
                                }
                            },
                            "description": "OK",
                        }
                    },
                    "tags": ["API-v2"],
                }
            }
        },
        "components": {
            "schemas": {
                "Podcast": {
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
                        "explicit": {"type": "boolean"},
                        "image": {"type": "string"},
                        "key": {"type": "string"},
                        "keywords": {
                            "items": {"type": "string"},
                            "type": "array",
                            "uniqueItems": True,
                        },
                        "language": {"type": "string"},
                        "link": {"type": "string"},
                        "ownerEmail": {"type": "string"},
                        "ownerName": {"type": "string"},
                        "showType": {"type": "string"},
                        "subtitle": {"type": "string"},
                        "summary": {"type": "string"},
                        "title": {"type": "string"},
                    },
                    "required": [
                        "categories",
                        "description",
                        "language",
                        "summary",
                        "title",
                    ],
                    "type": "object",
                }
            }
        },
    }


def settings_mock():
    return {
        "functions_to_endpoints": {
            "/api/v2/podcasts/create": "TestClass",
            "update_time_interval": 500,
        }
    }
