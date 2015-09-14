# encoding=utf8


def get_dict_value(d, name, defvalue=''):
    if name in d:
        return d[name]
    return defvalue


class BaseData (object):

    def __init__(self, data):
        self.errorCode = 1
        pass

    def has_error(self):
        """判断数据是否有错误"""
        return self.errorCode != 0

    def get_title(self):
        return ''

    def get_phonetic(self):
        return ''

    def get_basic(self):
        """返回基本释义的列表"""
        return ['']

    def get_extra(self):
        """返回额外解释的列表，包含健和值"""
        return [{'key': '', 'value': ''}]
