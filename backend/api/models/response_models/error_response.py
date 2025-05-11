from api.models.response_models.base_response import BaseResponseModel


class ErrorResponse(BaseResponseModel):
	error: str
