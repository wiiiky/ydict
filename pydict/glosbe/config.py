# encoding=utf8

from ..base import config


class Config (config.BaseConfig):

    FROM = 'eng'
    DEST = 'zh'
    GLOSBE_URL = "https://glosbe.com/gapi/translate?from=%s&dest=%s&format=json&phrase=%s&pretty=true"

    @staticmethod
    def build_url(q):
        url = Config.GLOSBE_URL % (Config.FROM, Config.DEST, q)
        return url

    @staticmethod
    def get_options():
        return {
            'zh->en': Config.zh_eng,
            'en->zh': Config.eng_zh
        }

    @staticmethod
    def get_option():
        if Config.FROM == 'eng':
            return 'en->zh'
        return 'zh->en'

    @staticmethod
    def eng_zh():
        Config.FROM = 'eng'
        Config.DEST = 'zh'

    @staticmethod
    def zh_eng():
        Config.FROM = 'zh'
        Config.DEST = 'eng'
