class SchemaServices:
    schema = []

    def __init__(self):
        pass

    @classmethod
    def load_components(cls, components: dict):
        cls.components = components

    @classmethod
    def add_endpoint(cls, endpoint):
        cls.schema.append(endpoint)

    @classmethod
    def find_schema(cls, schema):
        ref = schema["$ref"].split("/")[1:]
        actual = cls.components
        for item in ref:
            actual = actual[item]
        return actual

    @classmethod
    def turn_schema(cls, base_schema: dict, study_schema: dict):
        for key in study_schema.keys():
            if "$ref" in key:
                base_schema = {
                    **base_schema,
                    **cls.turn_schema(
                        base_schema, cls.find_schema(study_schema)
                    ),
                }
            elif isinstance(study_schema[key], dict) or key == "properties":
                base_schema[key] = cls.turn_schema({}, study_schema[key])
            elif isinstance(study_schema[key], list) and key in [
                'allOf',
                "oneOf",
                "anyOf",
            ]:
                base_schema[key] = []
                for item in study_schema[key]:
                    base_schema[key].append(cls.turn_schema({}, item))
            else:
                base_schema[key] = study_schema[key]
        return base_schema

    @classmethod
    def build(cls, schema: dict):
        if "content" in schema:
            key = next(iter(schema['content']))
            study_schema = schema['content'][key]["schema"]
            base_schema = cls.turn_schema({}, study_schema)
            return {
                "content_type": key,
                "schema": base_schema,
            }
        if "$ref" in schema:
            base = cls.turn_schema({}, cls.find_schema(schema))
            return cls.build(base)
        return {"content_type": "*/*", "description": schema["description"]}
