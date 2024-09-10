import logging
from urllib.parse import parse_qs

from jsonschema import ValidationError, validate

from middleware.exceptions import ValidationErrorException

logger = logging.getLogger(__name__)


class CheckParams:

    @staticmethod
    async def transfrom_query_params(query_params):
        return dict(
            (k, v if len(v) > 1 else v[0])
            for k, v in parse_qs(query_params, keep_blank_values=True).items()
        )

    @staticmethod
    async def headers_query_params(
        rules_dict: dict, params_dict: dict, position: str
    ) -> None:
        """
        This function checks if all "required" keys from first_dict match
        the keys in second_dict.
        """
        try:
            if position == "path-params" and "" in params_dict.values():
                raise ValidationError(
                    "Path parameters cannot be empty",
                    instance=params_dict,
                    schema=rules_dict,
                )
            validate(
                instance=params_dict,
                schema=rules_dict,
            )
        except ValidationError as e:
            pointer = [position]
            pointer.extend(e.json_path.split("."))
            errors = [
                {
                    "detail": e.message,
                    "pointer": pointer,
                }
            ]
            raise ValidationErrorException(errors) from e
