# encoding=utf8


from ..base import config


class Config (config.BaseConfig):

    FROM = 'en'
    TO = 'zh'
    BAIDU_URL = 'http://apis.baidu.com/apistore/tranlateservice/dictionary?from=%s&to=%s&query=%s'

    @staticmethod
    def build_url(q):
        return Config.BAIDU_URL % (Config.FROM, Config.TO, q)

    @staticmethod
    def build_headers():
        return {
            'apikey': '0138d28734a017dabdfaf5c15de9be8f'
        }

    @staticmethod
    def get_options():
        return {
            'zh->en': Config.zh_en,
            'en->zh': Config.en_zh
        }

    @staticmethod
    def get_option():
        if Config.FROM == 'en':
            return 'en->zh'
        return 'zh->en'

    @staticmethod
    def en_zh():
        Config.FROM = 'en'
        Config.DEST = 'zh'

    @staticmethod
    def zh_en():
        Config.FROM = 'zh'
        Config.DEST = 'en'
