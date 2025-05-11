from api.tests.fixtures.endpoints_test_data import (
    create_test_user,
    fast_api_test_app,
    user_authentication_header,
    create_test_movie,
    create_test_rating,
)

client = fast_api_test_app()


def test_when_movies_exists_then_return_movies_data():
    create_test_user(password='test', count=2)
    create_test_movie(count=5)
    create_test_rating(1, 1, 4)
    create_test_rating(2, 1, 3)
    create_test_rating(1, 2, 3)
    create_test_rating(2, 2, 2)

    response = client.get('/api/movie', headers=user_authentication_header())
    response_as_json = response.json()
    assert response.status_code == 200
    assert len(response_as_json['movies']) == 5
    assert response_as_json['movies'] == [
        {
            'id': 5,
            'title': 'test_movie_4',
            'description': 'dummy description',
        },
        {
            'id': 4,
            'title': 'test_movie_3',
            'description': 'dummy description',
        },
        {
            'id': 3,
            'title': 'test_movie_2',
            'description': 'dummy description',
        },
        {
            'id': 2,
            'title': 'test_movie_1',
            'rating': 2.5,
            'description': 'dummy description',
        },
        {
            'id': 1,
            'title': 'test_movie_0',
            'rating': 3.5,
            'description': 'dummy description',
        },
    ]


def test_when_movie_exists_then_return_single_movie_data_response():
    create_test_user(password='test', count=2)
    create_test_movie(count=5)
    create_test_rating(2, 1, 3)
    create_test_rating(2, 2, 2)

    response = client.get('/api/movie/2', headers=user_authentication_header())
    response_as_json = response.json()
    assert response.status_code == 200
    assert response_as_json == {
        'id': 2,
        'title': 'test_movie_1',
        'rating': 2.5,
        'description': 'dummy description',
    }


def test_when_movie_not_exists_then_return_single_error_response():
    create_test_user(password='test', count=2)
    create_test_movie(count=1)

    response = client.get('/api/movie/2', headers=user_authentication_header())
    response_as_json = response.json()
    assert response.status_code == 404
    assert response_as_json['error'] == 'Movie not found'


def test_when_valid_create_request_is_handled_then_create_new_movie():
    create_test_user(password='test', count=2)
    create_test_movie(count=1)

    response = client.post(
        '/api/movie',
        headers=user_authentication_header(),
        json={'title': 'new movie', 'description': 'test', 'release_year': '2008'},
    )
    response_as_json = response.json()
    assert response.status_code == 200
    assert response_as_json == {
        'id': 2,
        'title': 'new movie',
        'rating': 0.0,
        'description': 'test',
    }


def test_when_invalid_user_credential_is_passed_then_return_error_response():
    create_test_user(password='test', count=2)
    create_test_movie(count=1)
    response = client.post(
        '/api/movie',
        headers=user_authentication_header('test_10'),
        json={'title': 'new movie', 'description': 'test', 'release_year': '2008'},
    )
    assert response.status_code == 401
