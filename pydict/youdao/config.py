# encoding=utf8


YOUDAO_KEY = '619541059'
YOUDAO_KEYFROM = 'github-wdict'
YOUDAO_URL = 'http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=' % (
    YOUDAO_KEYFROM, YOUDAO_KEY)


def build_url(q):
    url = YOUDAO_URL + q
    return url
