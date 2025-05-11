from api.tests.fixtures.endpoints_test_data import (
    create_test_user,
    fast_api_test_app,
    user_authentication_header,
    create_test_movie,
    create_test_rating,
)

client = fast_api_test_app()


def test_when_valid_create_request_is_handled_then_create_new_rating():
    create_test_user(password='test')
    create_test_movie(count=1)

    response = client.post(
        '/api/rating',
        headers=user_authentication_header(),
        json={'rating': 2, 'movie_info_id': 1, 'user_info_id': 1},
    )
    response_as_json = response.json()
    assert response.status_code == 200
    assert response_as_json == {
        'id': 1,
        'rating': 2,
        'movie_info': {
            'description': 'dummy description',
            'id': 1,
            'title': 'test_movie_0',
        },
        'user_info': {'active': True, 'username': 'test'},
    }


def test_when_invalid_user_credential_is_passed_then_return_error_response():
    create_test_user(password='test', count=2)
    create_test_movie(count=1)
    response = client.post(
        '/api/rating',
        headers=user_authentication_header('test_10'),
        json={'rating': 2, 'movie_info_id': 1, 'user_info_id': 1},
    )
    assert response.status_code == 401


def test_when_get_ratings_for_user_is_called_then_return_the_respective_response():
    create_test_user(password='test', count=2)
    create_test_movie(count=2)
    create_test_rating(1, 1, 3)
    create_test_rating(2, 1, 3)
    response = client.get('/api/rating/user', headers=user_authentication_header())
    response_as_json = response.json()
    print(response_as_json)
    assert response.status_code == 200
    assert response_as_json == {
        'ratings': [
            {
                'id': 1,
                'rating': 3,
                'movie_info': {
                    'id': 1,
                    'title': 'test_movie_0',
                    'description': 'dummy description',
                },
                'review': '',
            },
            {
                'id': 2,
                'rating': 3,
                'movie_info': {
                    'id': 2,
                    'title': 'test_movie_1',
                    'description': 'dummy description',
                },
                'review': '',
            },
        ],
        'total_count': 0,
    }


def test_when_get_rating_for_movie_is_called_then_return_the_respective_response():
    create_test_user(password='test')
    create_test_movie(count=10)
    create_test_rating(7, 1, 3)
    response = client.get('/api/rating/movie/7', headers=user_authentication_header())
    response_as_json = response.json()
    assert response.status_code == 200
    assert response_as_json == {
        'id': 1,
        'rating': 3,
        'movie_info': {
            'id': 7,
            'title': 'test_movie_6',
            'description': 'dummy description',
        },
    }
