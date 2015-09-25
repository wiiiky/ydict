# encoding=utf8


import importlib
from . import config


def get_config():
    mod = importlib.import_module('%s.config' % config.API)
    return mod.Config


def get_data():
    mod = importlib.import_module('%s.data' % config.API)
    return mod.ResultData
