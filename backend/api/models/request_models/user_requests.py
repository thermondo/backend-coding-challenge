from pydantic import BaseModel


class CreateUserAPIRequest(BaseModel):
	name: str
	password: str

	class Config:
		json_schema_extra = {
			'example': {
				'name': 'Dark night',
				'password': '***',
			}
		}


class ChangePasswordAPIRequest(BaseModel):
	name: str
	old_password: str
	password: str

	class Config:
		json_schema_extra = {
			'example': {'name': 'Dark night', 'password': '***', 'old_password': '***'}
		}


class ForgotPasswordAPIRequest(BaseModel):
	name: str

	class Config:
		json_schema_extra = {
			'example': {
				'name': 'Dark night',
			}
		}


class ActivationRequest(BaseModel):
	name: str
	token: str

	class Config:
		json_schema_extra = {'example': {'name': 'Dark night', 'token': 'activation token'}}
