from typing import List

from middleware.schemas import ErrorModel


class NotFoundError(Exception):

    def __init__(self, value: List[ErrorModel]):
        self._errors = value

    def errors(self):
        return self._errors


class ValidationErrorException(Exception):
    def __init__(self, value: List[ErrorModel]):
        self._errors = value

    def errors(self):
        return self._errors


class MethodNotAllowed(Exception):
    def __init__(self, value: List[ErrorModel]):
        self._errors = value

    def errors(self):
        return self._errors
