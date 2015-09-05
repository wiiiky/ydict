# encoding=utf8


GLOSBE_URL = "https://glosbe.com/gapi/translate?from=eng&dest=zh&format=json&phrase=%s&pretty=true"


def build_url(q):
    url = GLOSBE_URL % q
    return url
