'''Тестируем API https://jsonplaceholder.typicode.com/'''
import random
import requests
import pytest


class APIClient:
    '''Клиент для работы с API.'''

    def __init__(self, base_address='https://jsonplaceholder.typicode.com'):
        self.base_address = base_address

    def get_response(self, path):
        '''Получаем в качестве ответа словарь по заданному пути.'''
        response = requests.get(self.base_address + str(path)).json()
        return response


class TestAPI:
    '''5 тестов для API.'''

    def test_response_from_server_is_ok(self):
        '''Код ответа от сервера должен быть меньше 400.'''
        assert requests.get(APIClient().base_address).ok

    def test_list_of_post_is_100(self):
        '''Сервер должен возвращать 100 уникальных постов.'''
        response = APIClient.get_response(APIClient(), '/posts')
        assert len(response) == 100

    def test_no_same_user_id(self):
        '''Сервер должен возвращать данные о пользовтелях.

        ID пользовталей не должны повторяться.'''
        user_id_list = []
        response = APIClient.get_response(APIClient(), '/users')
        for i in range(len(response) - 1):
            user_id_list.append(response[i]['id'])
        assert len(user_id_list) == len(set(user_id_list))

    @pytest.mark.parametrize('post_number', [random.randint(0, 100) for _ in range(2)])
    def test_number_of_posts_equal_to_requested(self, post_number):
        '''Сервер должен возвращать данные о постах.

        ID постов должны соответствовать переданным значениям.'''
        response = APIClient.get_response(APIClient(), '/posts')[post_number]
        assert response['id'] == post_number + 1

    @pytest.mark.parametrize('post_number', [random.randint(0, 100) for _ in range(2)])
    def test_random_post_contains_4_fields(self, post_number):
        '''Сервер должен возвращать данные о постах.

        В каждом посте должны быть 4 обязательных поля.'''
        response = APIClient.get_response(APIClient(), '/posts')[post_number]
        assert not (response.keys() ^ ['userId', 'id', 'title', 'body'])


def main():
    pass


if __name__ == '__main__':
    main()
