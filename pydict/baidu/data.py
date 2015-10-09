# encoding=utf-8


from ..base import data


class ResultData (data.BaseData):

    def __init__(self, data):
        self.errorCode = data['errNum']
        if self.errorCode != 0:
            return
        self.result = data['retData']['dict_result']

    def get_title(self):
        return self.result['word_name']

    def get_phonetic(self):
        for sym in self.result['symbols']:
            if 'ph_am' in sym:
                return sym['ph_am']
            elif 'ph_en' in sym:
                return sym['ph_en']
        return ''

    def get_basic(self):
        basic = []
        for sym in self.result['symbols']:
            for part in sym['parts']:
                basic.extend(part['means'])
        return basic

    def get_extra(self):
        return []
