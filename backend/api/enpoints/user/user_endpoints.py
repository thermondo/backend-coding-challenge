from typing import Any, Optional, Union

import string
import random

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordRequestForm
from injector import Injector
from starlette.requests import Request
from typing_extensions import Annotated

from api.models.response_models.base_response import ResponseModel
from api.interactors.user_interactor import (
	UserInfoInteractor,
	oauth2_scheme,
	PasswordResponseMessageType,
	ActivateAccountResponseMessageType,
)
from api.enpoints.interfaces import EndPoint
from api.models.request_models.user_requests import (
	CreateUserAPIRequest,
	ChangePasswordAPIRequest,
	ForgotPasswordAPIRequest,
)
from api.models.response_models.error_response import ErrorResponse
from api.models.response_models.user_info_response import (
	SignUpResponse,
	SignUpStatus,
	ActivateAccountResponse,
	ChangePasswordResponse,
)

from domain_models.user_info import UserInfoModel
from enviroment import ACCESS_TOKEN_EXPIRE_MINUTES, ACTIVATION_CODE_SEP
from repository.models import (
	CreateUserInfoRequest,
	UpdateUserInfoRequest,
)
from repository.unit_of_work import Repositories, SQLAlchemyUnitOfWork
from utils import make_timestamp, from_timestamp
from logger import init_logger

logger = init_logger(__name__)
PUNCTUATION = r"""$*-.:@[]^|~"""


class UserInfoEndPoint(EndPoint):
	def __init__(self, injector: Injector) -> None:
		"""Initialize the User EndPoint with the required dependencies."""
		super().__init__()
		self._unit_of_work = injector.get(SQLAlchemyUnitOfWork)
		self._user_interactor = injector.get(UserInfoInteractor)

	async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
		"""
		Authenticates a user and returns a JWT access token if successful.
		Raises:
		    HTTPException: If authentication fails or user is inactive.
		Returns:
		    dict: Access token and token type.
		"""
		user_info_authenticated = self._user_interactor.authenticate_user(
			form_data.username, form_data.password
		)
		if not user_info_authenticated or not user_info_authenticated.active:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail='Incorrect username or password',
				headers={'WWW-Authenticate': 'Bearer'},
			)
		access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000
		access_token = self._user_interactor.create_access_token(
			data={'sub': user_info_authenticated.name},
			expires_delta=access_token_expires,
		)
		return {'access_token': access_token, 'token_type': 'Bearer'}

	async def sign_up(self, user_data: CreateUserAPIRequest) -> ResponseModel:
		"""
		Registers a new user and sends an activation code.
		Args:
		    user_data (Request): The incoming HTTP request containing user registration data.
		Returns:
		    ResponseModel: The response indicating success or failure of the registration.
		"""
		try:

			def select_transaction(
				repositories: Repositories,
			) -> Optional[UserInfoModel]:
				return repositories.user_info.select_user_by_name(user_data.name)

			user_info_model = self._unit_of_work.perform(select_transaction)
			if user_info_model is not None:
				return ResponseModel(
					SignUpResponse(
						user=self._user_interactor.to_user_response(user_info_model),
						message='User already exists',
						status=SignUpStatus.ALREADY_EXISTS.value,
					)
				)
			activation_code = ''.join(
				random.choices(string.ascii_uppercase + string.digits + PUNCTUATION, k=20)
			)
			create_request = CreateUserInfoRequest(
				name=user_data.name,
				password=user_data.password,
				activation_code=activation_code,
				activation_expiry_date=make_timestamp() + (60 * 60 * 1000),
				active=True,  # TODO: user account should be deactivate initially and activated later by verified email.
				#       , will be slipped for demonstration
			)

			def create_transaction(repositories: Repositories) -> UserInfoModel:
				return repositories.user_info.create_user(create_request)

			user_info_model = self._unit_of_work.perform(create_transaction)

			# TODO: Email message with the verification token must be sent to the user

			return ResponseModel(
				SignUpResponse(
					user=self._user_interactor.to_user_response(user_info_model),
					message='User created successfully',
					status=SignUpStatus.SUCCEED.value,
				)
			)
		except Exception as err:
			logger.error(f'Error while signing up: {err}')
			return ResponseModel(
				SignUpResponse(
					status_code=500,
					user=None,
					message='Error while creating user',
					status=SignUpStatus.FAILED.value,
				)
			)

	async def generate_activation_code(self, name: str) -> ResponseModel:
		"""
		Generates a new activation code for an existing user.
		Args:
		    name (str): The name of the user for whom the activation code is generated.
		Returns:
		    ResponseModel: The response indicating success or failure of the activation code generation.
		"""
		try:

			def select_transaction(
				repositories: Repositories,
			) -> Optional[UserInfoModel]:
				return repositories.user_info.select_user_by_name(name)

			user_info_model = self._unit_of_work.perform(select_transaction)
			if user_info_model is None:
				return ResponseModel(
					ActivateAccountResponse(
						user=None,
						message=self._user_interactor.get_activated_response_message(
							ActivateAccountResponseMessageType.NO_USER
						),
						isActivated=False,
					)
				)
			activation_code = ''.join(
				random.choices(string.ascii_uppercase + string.digits + PUNCTUATION, k=20)
			)

			update_request = UpdateUserInfoRequest(
				id=user_info_model.id,
				activation_code=activation_code,
				activation_expiry_date=make_timestamp() + (60 * 60 * 1000),
				active=user_info_model.active,
			)

			def update_transaction(repositories: Repositories) -> UserInfoModel:
				return repositories.user_info.update_user(update_request)

			user_info_model = self._unit_of_work.perform(update_transaction)

			# TODO: Email message with the activation code must be sent to the user

			return ResponseModel(
				ActivateAccountResponse(
					user=self._user_interactor.to_user_response(user_info_model),
					message=self._user_interactor.get_activated_response_message(
						ActivateAccountResponseMessageType.LINK_IS_GENERATED
					),
					isActivated=True,
				)
			)
		except Exception as err:
			logger.error(f'Error while generating activation code: {err}')
			return ResponseModel(
				ActivateAccountResponse(
					status_code=500,
					user=None,
					message=self._user_interactor.get_activated_response_message(
						ActivateAccountResponseMessageType.FAILED_LINK_GENERATED
					),
					isActivated=False,
				)
			)

	async def activate_account(self, token: str) -> ResponseModel:
		"""
		Activates a user's account using the provided activation token.

		This method validates the provided token, checks the expiration, and activates
		the user account if the token is correct and within its expiry time.

		Args:
		    token (str): The activation token received by the user.

		Returns:
		    ResponseModel: The response indicating success or failure of the activation code.
		        - If the user is not found, returns a 404 with a 'No user' message.
		        - If the account is already activated, returns a response indicating that.
		        - If the token is valid and within expiry, activates the account and returns success.
		        - If the token is invalid or expired, returns a 404 with a 'Code not valid' message.
		        - If an error occurs, returns a 500 response with a failure message.
		"""
		try:
			activation_data = self._user_interactor.get_activation_data(token)

			def select_transaction(
				repositories: Repositories,
			) -> Optional[UserInfoModel]:
				return repositories.user_info.select_user_by_name(activation_data.name)

			user_info_model = self._unit_of_work.perform(select_transaction)
			if user_info_model is None:
				return ResponseModel(
					ActivateAccountResponse(
						status_code=404,
						user=None,
						message=self._user_interactor.get_activated_response_message(
							ActivateAccountResponseMessageType.NO_USER
						),
						isActivated=False,
					)
				)

			if user_info_model.active:
				return ResponseModel(
					ActivateAccountResponse(
						user=self._user_interactor.to_user_response(user_info_model),
						message=self._user_interactor.get_activated_response_message(
							ActivateAccountResponseMessageType.ALREADY_ACTIVATED
						),
						isActivated=False,
					)
				)

			if (
				user_info_model.activation_expiry_date > from_timestamp(make_timestamp())
				and user_info_model.activation_code == activation_data.token
			):
				update_request = UpdateUserInfoRequest(id=user_info_model.id, active=True)

				def update_transaction(repositories: Repositories) -> UserInfoModel:
					return repositories.user_info.update_user(update_request)

				user_info_model = self._unit_of_work.perform(update_transaction)
				return ResponseModel(
					ActivateAccountResponse(
						user=self._user_interactor.to_user_response(user_info_model),
						message=self._user_interactor.get_activated_response_message(
							ActivateAccountResponseMessageType.SUCCEED
						),
						isActivated=True,
					)
				)
			else:
				return ResponseModel(
					ActivateAccountResponse(
						status_code=404,
						user=self._user_interactor.to_user_response(user_info_model),
						message=self._user_interactor.get_activated_response_message(
							ActivateAccountResponseMessageType.CODE_NOT_VALID
						),
						isActivated=False,
					)
				)
		except Exception as err:
			logger.error(f'Error while activating user account: {err}')
			return ResponseModel(
				ActivateAccountResponse(
					status_code=500,
					user=None,
					message=self._user_interactor.get_activated_response_message(
						ActivateAccountResponseMessageType.FAILED
					),
					isActivated=False,
				)
			)

	async def change_password(self, user_data: ChangePasswordAPIRequest) -> ResponseModel:
		"""
		Changes the password of a user.

		This method validates the old password, checks if the user exists, and updates
		the password if the old password matches the stored activation code. If successful,
		the password is changed. Otherwise, appropriate error messages are returned.

		Args:
		    user_data (Request): The incoming HTTP request containing the user data (username and old/new password).

		Returns:
		    ResponseModel: The response indicating success or failure of the changing password process.
		        - If the user does not exist, returns a 404 with a 'No user' message.
		        - If the old password does not match the activation code, returns a 404 with a 'Password not matched' message.
		        - If the password is successfully changed, returns a success message with user data.
		        - If an error occurs, returns a 404 response with a failure message.
		"""
		try:

			def select_transaction(
				repositories: Repositories,
			) -> Optional[UserInfoModel]:
				return repositories.user_info.select_user_by_name(user_data.name)

			user_info_model = self._unit_of_work.perform(select_transaction)
			if user_info_model is None:
				return ResponseModel(
					ChangePasswordResponse(
						status_code=404,
						user=None,
						message=self._user_interactor.get_password_changed_response_message(
							PasswordResponseMessageType.NO_USER
						),
						isChanged=False,
					)
				)

			if user_info_model.activation_code != user_data.old_password:
				return ResponseModel(
					ChangePasswordResponse(
						status_code=404,
						user=self._user_interactor.to_user_response(user_info_model),
						message=self._user_interactor.get_password_changed_response_message(
							PasswordResponseMessageType.NOT_MATCHED
						),
						isChanged=False,
					)
				)
			update_request = UpdateUserInfoRequest(
				id=user_info_model.id,
				password=user_data.password,
				active=user_info_model.active,
			)

			def update_transaction(repositories: Repositories) -> UserInfoModel:
				return repositories.user_info.update_user(update_request)

			user_info_model = self._unit_of_work.perform(update_transaction)
			return ResponseModel(
				ChangePasswordResponse(
					user=self._user_interactor.to_user_response(user_info_model),
					message=self._user_interactor.get_password_changed_response_message(
						PasswordResponseMessageType.SUCCEED
					),
					isChanged=True,
				)
			)
		except Exception as err:
			logger.error(f'Error while changing password: {err}')
			return ResponseModel(
				ChangePasswordResponse(
					status_code=404,
					user=None,
					message=self._user_interactor.get_password_changed_response_message(
						PasswordResponseMessageType.FAILED
					),
					isActivated=False,
				)
			)

	async def forgot_password(self, user_data: ForgotPasswordAPIRequest) -> ResponseModel:
		"""
		Initiates a password reset process by generating a new activation code for the user.

		This method checks if the user exists and generates a new activation code, which can
		be used to reset the password. An email with the activation code should be sent to the user.

		Args:
		    user_data (Request): The incoming HTTP request containing the user data (username).

		Returns:
		    ResponseModel: A response indicating the result of the password reset process.
		        - If the user does not exist, returns a 404 with a 'No user' message.
		        - If the activation code is generated successfully, returns a success message with user data.
		        - If an error occurs, returns a 500 response with a failure message.
		"""
		try:

			def select_transaction(
				repositories: Repositories,
			) -> Optional[UserInfoModel]:
				return repositories.user_info.select_user_by_name(user_data.name)

			user_info_model = self._unit_of_work.perform(select_transaction)
			if user_info_model is None:
				return ResponseModel(
					ChangePasswordResponse(
						status_code=404,
						user=None,
						message=self._user_interactor.get_password_changed_response_message(
							PasswordResponseMessageType.NO_USER
						),
						isChanged=False,
					)
				)

			activation_code = ''.join(
				random.choices(string.ascii_uppercase + string.digits + PUNCTUATION, k=20)
			)

			update_request = UpdateUserInfoRequest(
				id=user_info_model.id,
				activation_code=activation_code,
				activation_expiry_date=make_timestamp() + (60 * 60 * 1000),
				active=user_info_model.active,
			)

			def update_transaction(repositories: Repositories) -> UserInfoModel:
				return repositories.user_info.update_user(update_request)

			user_info_model = self._unit_of_work.perform(update_transaction)

			# TODO: Email message with the activation code must be sent to the user

			return ResponseModel(
				ChangePasswordResponse(
					user=self._user_interactor.to_user_response(user_info_model),
					message=self._user_interactor.get_password_changed_response_message(
						PasswordResponseMessageType.SUCCEED
					),
					isChanged=True,
				)
			)
		except Exception as err:
			logger.error(f'Error while processing forgot password request: {err}')
			return ResponseModel(
				ChangePasswordResponse(
					status_code=500,
					user=None,
					message=self._user_interactor.get_password_changed_response_message(
						PasswordResponseMessageType.FAILED
					),
					isActivated=False,
				)
			)

	async def sign_out(self) -> Union[Any, ErrorResponse]:
		# TODO: sign out functionality must verify the user validity using the authorisation token
		return {
			'signout': True,
		}

	def validate_session(self, token: Annotated[str, Depends(oauth2_scheme)]) -> Response:
		try:
			if self._user_interactor.is_valid_user(token):
				user_info = self._user_interactor.get_current_user_info(token)
				return ResponseModel(self._user_interactor.to_user_response(user_info))
		except Exception as err:  # pylint: disable=W0718
			logger.error(f'Error while validating session: {err}')
			return ResponseModel(ErrorResponse(error='unknown error', status_code=401))
		return ResponseModel(ErrorResponse(error='unknown error', status_code=401))

	def router(self) -> APIRouter:
		router = APIRouter(
			prefix='/auth',
			tags=['Authentication'],
		)
		router.add_api_route('/signin', self.login, methods=['POST'])
		router.add_api_route('/signup', self.sign_up, methods=['POST'])
		router.add_api_route('/signout', self.sign_out, methods=['POST'])
		router.add_api_route('/{token}', self.activate_account, methods=['GET'])
		router.add_api_route('/generate/{name}', self.generate_activation_code, methods=['GET'])
		router.add_api_route('/password', self.change_password, methods=['POST'])
		router.add_api_route('/forgotpassword', self.forgot_password, methods=['POST'])
		router.add_api_route('/validate', self.validate_session, methods=['POST'])
		return router
