# encoding=utf8


def get_dict_value(d, name, defvalue=''):
    if name in d:
        return d[name]
    return defvalue


class ResultData (object):

    def __init__(self, data):
        self.errorCode = 1
        pass

    def has_error(self):
        """判断数据是否有错误"""
        return self.errorCode != 0

    def title(self):
        return ''
