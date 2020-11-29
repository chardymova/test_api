import pytest


def pytest_addoption(parser):
    '''Передаем различные значения зависимости от параметров командной строки.'''

    parser.addoption('--url',
                     action='store',
                     default='https://yandex.ru',
                     help='This is request url')


@pytest.fixture
def url_param(request):
    '''Получаем параметр, введенный в командную строку.'''
    return request.config.getoption('--url')
