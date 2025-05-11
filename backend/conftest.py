import pytest

pytest_plugins = [
    'repository.tests.fixtures',
]


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'rpc',
        'CELERY_ALWAYS_EAGER': True,
    }
