# encoding=utf-8

from ..base import data as base


class ResultData (base.BaseData):

    def __init__(self, data):
        """data是一个JSON对象"""
        self.result = data['result']
        if self.result != 'ok':
            self.errorCode = 1
            return
        self.errorCode = 0
        self.query = base.get_dict_value(data, 'phrase')
        self.tuc = base.get_dict_value(data, 'tuc', [])

    def get_title(self):
        return self.query

    def get_phonetic(self):
        """没有音标"""
        return ''

    def get_basic(self):
        basic = []
        for tuc in self.tuc:
            if 'phrase' in tuc:
                text = tuc['phrase']['text']
                basic.append(text)
        return basic

    def get_extra(self):
        extra = []
        for tuc in self.tuc:
            if 'meanings' in tuc:
                for meaning in tuc['meanings']:
                    extra.append({'key': self.query, 'value': meaning['text']})
        return extra
