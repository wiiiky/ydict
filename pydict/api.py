# encoding=utf8


from pydict import youdao
from pydict.youdao import config as youdao_config
from pydict.youdao import data as youdao_data


API_SERVICE = youdao


def get_config():
    if API_SERVICE == youdao:
        return youdao_config


def get_data():
    if API_SERVICE == youdao:
        return youdao_data
