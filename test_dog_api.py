'''Тестируем API https://dog.ceo/dog-api/'''
import random
import requests
import pytest
from dog_api_list_of_breeds import list_of_breeds


class APIClient:
    '''Клиент для работы с API.'''

    def __init__(self, base_address='https://dog.ceo/api'):
        self.base_address = base_address

    def get_response(self, path):
        '''Получаем в качестве ответа словарь по заданному пути.'''
        r = requests.get(self.base_address + str(path)).json()
        return r

    def get_message(self, path):
        '''Получаем сообщение из запроса.'''
        message = self.get_response(path)['message']
        return message

    def get_status(self, path):
        '''Получаем статус запроса.'''
        status = self.get_response(path)['status']
        return str(status)

    def get_random_breed(self):
        '''Получаем случайную породу.'''
        path = '/breeds/list/all'
        all_breeds = self.get_response(path)['message']
        random_breed = random.choice(list(all_breeds.keys()))
        return random_breed

    def get_random_breed_pic(self, breed, path='/breed/{}/images/random'):
        '''Получаем случайную картинку породы.'''
        r = requests.get(self.base_address + path.format(breed)).json()['message']
        return r

    def get_sub_breed_list(self, breed, path='/breed/{}/list'):
        '''Получаем лист подпород для переданной породы.
        Может возвращать пустой лист,
        если для данной породы такие отсутствуют.

        '''
        r = requests.get(self.base_address + path.format(breed)).json()['message']
        return r

class TestAPI:
    '''5 тестов для API.'''

    @pytest.mark.parametrize('path',
                             ['/breeds/list/all', '/breeds/image/random', '/breeds/image/random/3'])
    def test_status_code(self, path):
        '''Сервер должен вовращать статус "success", если запрос выполнен успешно.'''
        status = APIClient.get_status(APIClient(), path)
        assert status == 'success'

    @pytest.mark.parametrize('breeds', [APIClient().get_random_breed() for _ in range(3)])
    def test_response_with_breed_pic_is_str(self, breeds):
        '''Сервер должен вовращать 1 случайную картинку собаки данной породы.

        Ссылка на картинку должна являтся str.
        '''
        pic = APIClient.get_random_breed_pic(APIClient(), breeds)
        assert isinstance(pic, str)

    @pytest.mark.parametrize('breeds', [APIClient().get_random_breed() for _ in range(3)])
    def test_response_to_breed_pic_is_success(self, breeds):
        '''Сервер должен вовращать 1 случайную картинку собаки данной породы.

        Ссылка на картинку должна являтся str.
        '''
        pic = APIClient.get_random_breed_pic(APIClient(), breeds)
        r=requests.get(pic).ok
        assert r

    @pytest.mark.parametrize('breeds', [APIClient().get_random_breed() for _ in range(3)])
    def test_sub_breed(self, breeds):
        '''Сервер должен вовращать лист подпород для переданной породы.'''
        sub_breed = APIClient.get_sub_breed_list(APIClient(), breeds)
        assert isinstance(sub_breed, list)

    def test_random_breed_is_in_breed_list(self):
        '''Случайная порода, возвращаемая сервером, должна входить в список пород.'''
        random_breed = APIClient.get_random_breed(APIClient())
        assert random_breed in list_of_breeds

def main():
    pass

if __name__ == '__main__':
    main()
