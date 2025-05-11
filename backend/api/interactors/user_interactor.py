from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from injector import Injector
from jose import JWTError, jwt

from api.models.request_models.user_requests import ActivationRequest
from api.models.response_models.user_info_response import TokenData, UserResponse
from domain_models.user_info import UserInfoModel
from enviroment import ALGORITHM, SECRET_KEY, ACTIVATION_CODE_SEP
from repository.unit_of_work import Repositories, SQLAlchemyUnitOfWork
from utils import make_timestamp, from_timestamp

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/signin')

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


class PasswordResponseMessageType(str, Enum):
    SUCCEED = 'SUCCEED'
    FAILED = 'FAILED'
    NOT_MATCHED = 'NOT_MATCHED'
    NO_USER = 'NO_USER'


class ActivateAccountResponseMessageType(str, Enum):
    SUCCEED = 'SUCCEED'
    FAILED = 'FAILED'
    NO_USER = 'NO_USER'
    CODE_NOT_VALID = 'CODE_NOT_VALID'
    ALREADY_ACTIVATED = 'ALREADY_ACTIVATED'
    LINK_IS_GENERATED = 'LINK_IS_GENERATED'
    FAILED_LINK_GENERATED = 'FAILED_LINK_GENERATED'


class UserInfoInteractor:
    """
    Interactor class for handling user authentication, token processing, and user management operations.

    This class provides functionality to authenticate users, retrieve current user information using a token,
    and manage user activation, password changes, and token creation. It interacts with the database through
    a unit of work pattern and supports JWT-based authentication.

    Attributes:
        _unit_of_work (SQLAlchemyUnitOfWork): The unit of work used to interact with the database repositories.
    """

    def __init__(self, injector: Injector) -> None:
        super().__init__()
        self._unit_of_work = injector.get(SQLAlchemyUnitOfWork)

    def authenticate_user(self, username: str, password: str) -> Optional[UserInfoModel]:
        """
        Authenticates a user based on the provided username and password.

        This method retrieves the user from the database by username and checks if the provided password matches
        the stored password. If authentication fails, it returns `None`.

        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            Optional[UserInfoModel]: The user info model if authentication succeeds, or `None` if it fails.
        """

        def transaction(repositories: Repositories) -> Optional[UserInfoModel]:
            return repositories.user_info.select_user_by_name(username)

        user_info = self._unit_of_work.perform(transaction)
        if not user_info or not user_info.hashed_password == password:
            return None
        return user_info

    def get_current_user_info(self, token: str) -> UserInfoModel:
        """
        Retrieves the current user's information from the token.

        This method decodes the JWT token to extract the username and retrieves the corresponding user information
        from the database. If the token is invalid or the user is not found, it raises an exception.

        Args:
            token (str): The JWT token containing the user’s authentication details.

        Returns:
            UserInfoModel: The user information model retrieved from the database.

        Raises:
            HTTPException: If the token is invalid or the user does not exist.
        """
        token_data: TokenData = self.get_token_data(token)
        user_name = token_data.username
        if not user_name:
            raise ValueError('Invalid token')

        def transaction(repositories: Repositories) -> Optional[UserInfoModel]:
            return repositories.user_info.select_user_by_name(user_name)

        user_info_in_db = self._unit_of_work.perform(transaction)
        if user_info_in_db is None:
            raise credentials_exception
        return user_info_in_db

    def get_current_user(self, token: str) -> UserResponse:
        """
        Retrieves the current user’s information in the form of a response model.

        This method decodes the JWT token to extract the username and returns the user response model. If the
        token is invalid or the user is not found, it raises an exception.

        Args:
            token (str): The JWT token containing the user’s authentication details.

        Returns:
            UserResponse: A user response model containing the user details.

        Raises:
            HTTPException: If the token is invalid or the user does not exist.
        """
        token_data: TokenData = self.get_token_data(token)
        user_name = token_data.username
        if not user_name:
            raise ValueError('Invalid token')

        def transaction(repositories: Repositories) -> Optional[UserInfoModel]:
            return repositories.user_info.select_user_by_name(user_name)

        user_info_in_db = self._unit_of_work.perform(transaction)
        if user_info_in_db is None:
            raise credentials_exception
        return self.to_user_response(user_info_in_db)

    def is_valid_user(self, token: str) -> bool:
        """
        Checks if the user corresponding to the token is valid.

        This method attempts to fetch the user by decoding the token. If the user is valid (exists in the database),
        it returns `True`; otherwise, it returns `False`.

        Args:
            token (str): The JWT token containing the user’s authentication details.

        Returns:
            bool: `True` if the user is valid, otherwise `False`.
        """
        try:
            if self.get_current_user(token):
                return True
            return False
        except HTTPException as err:
            print(err)
            return False

    @classmethod
    def get_token_data(cls, token: str) -> TokenData:
        """
        Decodes the JWT token and extracts the user data.

        This method decodes the JWT token to retrieve the username stored in the token. If the token is invalid or
        does not contain the expected data, it raises an exception.

        Args:
            token (str): The JWT token to decode.

        Returns:
            TokenData: The token data, including the username.

        Raises:
            HTTPException: If the token is invalid or missing expected data.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            username: str = payload.get('sub')
            if username is None:
                raise credentials_exception
            return TokenData(username=username)
        except JWTError as err:
            raise credentials_exception from err

    @classmethod
    def to_user_response(cls, user_info: UserInfoModel) -> UserResponse:
        """
        Converts a `UserInfoModel` to a `UserResponse` model.

        This method maps the user information model to a response model that can be returned in API responses.

        Args:
            user_info (UserInfoModel): The user information model to convert.

        Returns:
            UserResponse: The converted user response model.
        """
        return UserResponse(
            username=user_info.name, email=None, full_name=None, active=user_info.active
        )

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
        """
        Creates a JWT access token.

        This method creates an access token using the provided data and an optional expiration time. If no expiration
        time is provided, the default expiration is set to 15 minutes.

        Args:
            data (dict): The data to encode in the token.
            expires_delta (Optional[int]): The expiration time for the token in milliseconds (default is 15 minutes).

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = from_timestamp(make_timestamp() + expires_delta)
        else:
            expire = from_timestamp(make_timestamp() + (15 * 60 * 1000))
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_activation_data(data: str) -> ActivationRequest:
        """
        Extracts activation data from a string containing activation information.

        The data is expected to be in the format `username<separator>activation_code`. This method splits the string
        and returns an `ActivationRequest` object.

        Args:
            data (str): The activation data string to parse.

        Returns:
            ActivationRequest: The extracted activation data.
        """
        toke_data = data.split(ACTIVATION_CODE_SEP)
        return ActivationRequest(name=toke_data[0], token=toke_data[1])

    @staticmethod
    def get_password_changed_response_message(
        message_type: PasswordResponseMessageType,
    ) -> str:
        """
        Returns the response message corresponding to the given password change status.

        Args:
            message_type (PasswordResponseMessageType): The type of password change response.

        Returns:
            str: The response message.
        """
        if message_type == PasswordResponseMessageType.FAILED:
            return 'Error while changing password'
        elif message_type == PasswordResponseMessageType.SUCCEED:
            return 'Password is changed successfully'
        elif message_type == PasswordResponseMessageType.NO_USER:
            return 'User not exists'
        elif message_type == PasswordResponseMessageType.NOT_MATCHED:
            return "Password don't match"
        return ''

    @staticmethod
    def get_activated_response_message(
        message_type: ActivateAccountResponseMessageType,
    ) -> str:
        """
        Returns the response message corresponding to the given account activation status.

        Args:
            message_type (ActivateAccountResponseMessageType): The type of activation response.

        Returns:
            str: The response message.
        """
        if message_type == ActivateAccountResponseMessageType.FAILED:
            return 'Error while activating account'
        elif message_type == ActivateAccountResponseMessageType.SUCCEED:
            return 'Account is activated successfully'
        elif message_type == ActivateAccountResponseMessageType.NO_USER:
            return 'User not exists'
        elif message_type == ActivateAccountResponseMessageType.ALREADY_ACTIVATED:
            return 'User account is already activated'
        elif message_type == ActivateAccountResponseMessageType.CODE_NOT_VALID:
            return 'Activation code is not valid'
        elif message_type == ActivateAccountResponseMessageType.FAILED_LINK_GENERATED:
            return 'Error while generating Activation link'
        elif message_type == ActivateAccountResponseMessageType.LINK_IS_GENERATED:
            return 'Activation link is generated'
        return ''
