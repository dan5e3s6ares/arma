from typing import Any, List

from pydantic import BaseModel, ConfigDict, Field


class HeadersResponseModel(BaseModel):
    content_type: str = "application/problem+json"


class ErrorModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    detail: str = Field(alias="msg")
    pointer: List[Any] = Field(alias="loc")


class ErrorsModel(BaseModel):
    type: str
    title: str
    errors: List[ErrorModel]
