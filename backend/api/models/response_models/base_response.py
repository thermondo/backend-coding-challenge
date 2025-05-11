from typing import Any, Dict
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class BaseResponseModel(BaseModel):
    status_code: int = Field(exclude=True, default=200)

    def dict(  # noqa: D102
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        return super().model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=True,
        )

    def model_dump(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        return super().model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=True,
        )


class ResponseModel(JSONResponse):
    def __init__(self, response_base_model: BaseResponseModel):
        super(ResponseModel, self).__init__(
            content=response_base_model.dict(),
            status_code=response_base_model.status_code,
        )
