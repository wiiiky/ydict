# encoding=utf8


class BaseConfig (object):

    @staticmethod
    def build_url(q):
        return ''

    @staticmethod
    def get_options():
        return {}

    @staticmethod
    def get_option():
        return ''
