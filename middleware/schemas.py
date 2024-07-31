from typing import Any, List

from pydantic import BaseModel, Field


class HeadersResponseModel(BaseModel):
    content_type: str = "application/problem+json"


class ErrorModel(BaseModel):
    detail: str = Field(alias="msg")
    pointer: List[Any] = Field(alias="loc")


class ErrorsModel(BaseModel):
    type: str
    title: str
    errors: List[ErrorModel]
