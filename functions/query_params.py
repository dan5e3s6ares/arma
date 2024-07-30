from urllib.parse import parse_qs

from middleware.exceptions import ValidationErrorException


class CheckParams:

    @staticmethod
    async def transfrom_query_params(query_params):
        return dict(
            (k, v if len(v) > 1 else v[0])
            for k, v in parse_qs(query_params, keep_blank_values=True).items()
        )

    @staticmethod
    async def headers_query_params(rules_dict: dict, params_dict: dict):
        """
        This function checks if all "required" keys from first_dict match
        the keys in second_dict.
        """

        params_dict_keys = params_dict.keys()
        missing_fields = []

        for index, item in enumerate(rules_dict["required"]):
            if item.lower() not in params_dict_keys:
                missing_fields.append(
                    {"msg": "Missing Field", "loc": [index, item]}
                )

        if len(missing_fields) > 0:
            raise ValidationErrorException(missing_fields)
