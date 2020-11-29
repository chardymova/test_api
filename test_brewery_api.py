'''Тестируем API https://www.openbrewerydb.org'''
import random
import requests
import pytest


class APIClient:
    '''Клиент для работы с API.'''

    def __init__(self, base_address='https://api.openbrewerydb.org'):
        self.base_address = base_address

    def get_response(self, path):
        '''Получаем в качестве ответа словарь по заданному пути.'''
        response = requests.get(self.base_address + str(path)).json()
        return response


class TestAPI:
    '''5 тестов для API.'''
    global BREWERY_LIST
    BREWERY_LIST = APIClient.get_response(APIClient(), '/breweries')

    def test_list_of_breweries_is_list(self):
        '''Сервер должен вовращать список пивоваренных заводов.'''
        list_of_breweries = APIClient.get_response(APIClient(), '/breweries')
        assert isinstance(list_of_breweries, list)

    def test_item_in_the_list_of_breweries_is_dict(self):
        '''Сервер должен вовращать список пивоваренных заводов.

        Информация о каждом заводе должна быть представлена в виде словаря.'''
        list_of_breweries = APIClient.get_response(APIClient(), '/breweries')
        random_beer = list_of_breweries[random.randint(0, len(list_of_breweries) - 1)]
        assert isinstance(random_beer, dict)

    def test_standart_len_of_list_of_breweries_is_20(self):
        '''Сервер должен вовращать список пивоваренных заводов.

        Стандартная длина этого списка должна равнятся 20.'''
        list_of_breweries = APIClient.get_response(APIClient(), '/breweries')
        assert len(list_of_breweries) == 20

    @pytest.mark.parametrize('number_of_units_of_beer', [random.randint(1, 45) for _ in range(2)])
    def test_len_of_list_equal_to_requested(self, number_of_units_of_beer):
        '''Сервер должен вовращать список пивоваренных заводов.

         Длина списка должна быть равна переданному значению.'''
        list_of_breweries = APIClient.get_response(APIClient(),
                                                   '/breweries?per_page={}'.
                                                   format(number_of_units_of_beer))
        assert len(list_of_breweries) == number_of_units_of_beer

    @pytest.mark.parametrize('type_of_brewery', [BREWERY_LIST[random.randint(
        0, len(BREWERY_LIST) - 1)]['brewery_type'] for _ in range(2)])
    def test_type_of_brewery_equal_to_requested(self, type_of_brewery):
        '''Сервер должен вовращать список пивоваренных заводов.

         Тип пивоваренного завода должен соответствовать переданному значению.'''
        list_by_type = APIClient.get_response(APIClient(),
                                              '/breweries?by_type={}'.format(type_of_brewery))
        type_of_brewery_from_request = list_by_type[
            random.randint(0, len(list_by_type) - 1)]['brewery_type']
        assert type_of_brewery == type_of_brewery_from_request


def main():
    '''Главная функция.'''


if __name__ == '__main__':
    main()
