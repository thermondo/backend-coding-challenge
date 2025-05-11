from time import sleep

from api.models.response_models.user_info_response import (
    ChangePasswordResponse,
    UserResponse,
    ActivateAccountResponse,
)
from api.tests.fixtures.endpoints_test_data import (
    create_test_user,
    fast_api_test_app,
    user_authentication_header,
)
from api.interactors.user_interactor import (
    PasswordResponseMessageType,
    ActivateAccountResponseMessageType,
    UserInfoInteractor,
)
from enviroment import ACTIVATION_CODE_SEP
from utils import make_timestamp

client = fast_api_test_app()


def test_when_user_exists_then_password_can_be_can_changed():
    create_test_user(password='test')
    response = client.post(
        '/api/auth/password',
        headers=user_authentication_header(),
        json={'name': 'test', 'activation_code': 'test', 'password': 'test2'},
    )
    assert response.status_code == 200
    assert (
        response.json()
        == ChangePasswordResponse(
            user=UserResponse(username='test', email=None, full_name=None, active=True),
            message=UserInfoInteractor.get_password_changed_response_message(
                PasswordResponseMessageType.SUCCEED
            ),
            isChanged=True,
        ).dict()
    )


def test_when_user_not_exists_then_cannot_change_password():
    create_test_user(password='test')
    response = client.post(
        '/api/auth/password',
        headers=user_authentication_header(),
        json={'name': 'test_10', 'activation_code': 'test', 'password': 'test2'},
    )
    assert response.status_code == 404
    assert (
        response.json()
        == ChangePasswordResponse(
            user=None,
            message=UserInfoInteractor.get_password_changed_response_message(
                PasswordResponseMessageType.NO_USER
            ),
            isChanged=False,
        ).dict()
    )


def test_when_user_password_dont_match_then_cannot_change_password():
    create_test_user(password='test')
    response = client.post(
        '/api/auth/password',
        headers=user_authentication_header(),
        json={'name': 'test', 'activation_code': 'test10', 'password': 'test2'},
    )
    assert response.status_code == 404
    assert (
        response.json()
        == ChangePasswordResponse(
            user=UserResponse(username='test', email=None, full_name=None, active=True),
            message=UserInfoInteractor.get_password_changed_response_message(
                PasswordResponseMessageType.NOT_MATCHED
            ),
            isChanged=False,
        ).dict()
    )


def test_when_user_not_exists_then_cannot_generate_activation_link():
    create_test_user(password='test')
    response = client.get('/api/auth/generate/test_10', headers=user_authentication_header())
    assert response.status_code == 200
    assert (
        response.json()
        == ActivateAccountResponse(
            user=None,
            message=UserInfoInteractor.get_activated_response_message(
                ActivateAccountResponseMessageType.NO_USER
            ),
            isActivated=False,
        ).dict()
    )


def test_when_user_exists_then_generate_link():
    create_test_user(password='test')
    response = client.get('/api/auth/generate/test', headers=user_authentication_header())
    assert response.status_code == 200
    assert (
        response.json()
        == ActivateAccountResponse(
            user=UserResponse(username='test', email=None, full_name=None, active=True),
            message=UserInfoInteractor.get_activated_response_message(
                ActivateAccountResponseMessageType.LINK_IS_GENERATED
            ),
            isActivated=True,
        ).dict()
    )


def test_when_user_not_exists_then_cannot_activate():
    create_test_user(password='test', activation_code='test_token', active=False)
    response = client.get(
        '/api/auth/test_10' + ACTIVATION_CODE_SEP + 'test_token',
        headers=user_authentication_header(),
    )
    assert response.status_code == 404
    assert (
        response.json()
        == ActivateAccountResponse(
            user=None,
            message=UserInfoInteractor.get_activated_response_message(
                ActivateAccountResponseMessageType.NO_USER
            ),
            isActivated=False,
        ).dict()
    )


def test_when_user_exists_and_token_match_then_activate():
    new_time_stamp = make_timestamp() + (10 * 1000)
    create_test_user(
        password='test',
        activation_code='test_token',
        active=False,
        activation_expiry_date=new_time_stamp,
    )
    response = client.get(
        '/api/auth/test' + ACTIVATION_CODE_SEP + 'test_token',
        headers=user_authentication_header(),
    )
    assert response.status_code == 200
    assert (
        response.json()
        == ActivateAccountResponse(
            user=UserResponse(username='test', email=None, full_name=None, active=True),
            message=UserInfoInteractor.get_activated_response_message(
                ActivateAccountResponseMessageType.SUCCEED
            ),
            isActivated=True,
        ).dict()
    )


def test_when_user_exists_and_token_not_match_then_dont_activate():
    create_test_user(password='test', activation_code='test_token', active=False)
    response = client.get(
        '/api/auth/test' + ACTIVATION_CODE_SEP + 'test_token_no_match',
        headers=user_authentication_header(),
    )
    assert response.status_code == 404
    assert (
        response.json()
        == ActivateAccountResponse(
            user=UserResponse(username='test', email=None, full_name=None, active=False),
            message=UserInfoInteractor.get_activated_response_message(
                ActivateAccountResponseMessageType.CODE_NOT_VALID
            ),
            isActivated=False,
        ).dict()
    )


def test_when_user_exists_and_token_is_expired_then_dont_activate():
    old_time_stamp = make_timestamp() - (10 * 1000)
    create_test_user(
        password='test',
        activation_code='test_token',
        active=False,
        activation_expiry_date=old_time_stamp,
    )
    response = client.get(
        '/api/auth/test' + ACTIVATION_CODE_SEP + 'test_token',
        headers=user_authentication_header(),
    )
    assert response.status_code == 404
    assert (
        response.json()
        == ActivateAccountResponse(
            user=UserResponse(username='test', email=None, full_name=None, active=False),
            message=UserInfoInteractor.get_activated_response_message(
                ActivateAccountResponseMessageType.CODE_NOT_VALID
            ),
            isActivated=False,
        ).dict()
    )


def test_when_user_exists_and_already_activated_then_dont_activate():
    create_test_user(password='test', activation_code='test_token', active=True)
    response = client.get(
        '/api/auth/test' + ACTIVATION_CODE_SEP + 'test_token',
        headers=user_authentication_header(),
    )
    assert response.status_code == 200
    assert (
        response.json()
        == ActivateAccountResponse(
            user=UserResponse(username='test', email=None, full_name=None, active=True),
            message=UserInfoInteractor.get_activated_response_message(
                ActivateAccountResponseMessageType.ALREADY_ACTIVATED
            ),
            isActivated=False,
        ).dict()
    )
