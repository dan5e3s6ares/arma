class CheckParams:

    @staticmethod
    async def header_params(rules_dict: dict, params_dict: dict):

        missing_fields = {
            item.lower() for item in rules_dict["required"]
        }.issubset(set(params_dict.keys()))

        if not missing_fields:
            print(f"Missing fields: {missing_fields}")
            return False

        return True

    @staticmethod
    async def query_params(rules_dict: dict, params_dict: dict):
        """
        This function checks if all keys, their types and required values from first_dict
        match the top level keys, their types and "required" values in second_dict.
        """

        missing_fields = set(rules_dict["required"]) - set(params_dict.keys())

        if len(missing_fields) > 0:
            print(f"Missing fields: {missing_fields}")
            return False

        missing_fields = set(params_dict.keys()) - set(rules_dict["optional"])
        if len(missing_fields) > 0:
            print(f"Extra fields: {missing_fields}")
            return False

        return True
