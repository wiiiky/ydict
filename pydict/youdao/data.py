# encoding=utf8

from ..base import data as base


class ResultData (base.BaseData):

    def __init__(self, data):
        """data是一个JSON对象"""
        self.errorCode = data['errorCode']
        if self.errorCode != 0:
            return
        self.query = base.get_dict_value(data, 'query', 'good')
        self.translation = base.get_dict_value(data, 'translation', [])
        self.basic = base.get_dict_value(data, 'basic', {})
        self.web = base.get_dict_value(data, 'web', [])

    def get_title(self):
        return self.query

    def get_phonetic(self):
        if self.basic and 'us-phonetic' in self.basic:
            return self.basic['us-phonetic']
        return ''

    def get_basic(self):
        basic = []
        if self.basic:
            for explain in self.basic['explains']:
                basic.append(explain)
        if self.translation:
            for t in self.translation:
                basic.append(t)
        return basic

    def get_extra(self):
        extra = []
        for w in self.web:
            key = w['key']
            value = ', '.join(w['value'])
            extra.append({'key': key, 'value': value})
        return extra
