# encoding=utf8


import importlib


API = 'pydict.youdao'


def get_config():
    global API
    config = importlib.import_module('%s.config' % API)
    return config.Config


def get_data():
    global API
    data = importlib.import_module('%s.data' % API)
    return data.ResultData
