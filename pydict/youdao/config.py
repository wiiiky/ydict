# encoding=utf8


from ..base import config


class Config (config.BaseConfig):

    YOUDAO_KEY = '619541059'
    YOUDAO_KEYFROM = 'github-wdict'
    YOUDAO_URL = 'http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s'

    @staticmethod
    def build_url(q):
        return Config.YOUDAO_URL % (Config.YOUDAO_KEYFROM, Config.YOUDAO_KEY, q)
