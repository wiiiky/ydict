# encoding=utf8


from pydict.youdao import config as youdao_config
from pydict.youdao import data as youdao_data
from pydict.glosbe import config as glosbe_config
from pydict.glosbe import data as glosbe_data


API_SERVICES = {
    'youdao': {
        'config': youdao_config,
        'data': youdao_data
    },
    'glosbe': {
        'config': glosbe_config,
        'data': glosbe_data
    }
}

SERVICE_NAME = 'youdao'

def get_config():
    return API_SERVICES[SERVICE_NAME]['config']

def get_data():
    return API_SERVICES[SERVICE_NAME]['data']
