# encoding=utf8

from pydict.base import data as base


class ResultData (base.ResultData):

    def __init__(self, data):
        """data是一个JSON对象"""
        self.errorCode = data['errorCode']
        if self.errorCode != 0:
            return
        self.query = base.get_dict_value(data, 'query', 'good')
        self.translation = base.get_dict_value(data, 'translation', [])
        self.basic = base.get_dict_value(data, 'basic', {})
        self.web = base.get_dict_value(data, 'web', [])

    def title(self):
        return self.query
