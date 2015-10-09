# encoding=utf-8
# 执行查询

from gi.repository import Soup
from . import api
from . import log
from . import config
import json


SESSION = Soup.Session()


def callback(f, text, data, user_data):
    if user_data:
        f(text, data, user_data)
    else:
        f(text, data)


def on_read(stream, result, data):
    error = data['error']
    success = data['success']
    text = data['text']
    user_data = data['user_data']

    try:
        bytes = stream.read_bytes_finish(result)
        jdata = json.loads(str(bytes.get_data(), 'utf-8'))
        log.debug(str(jdata))
        data = api.get_data()(jdata)
        callback(success, text, data, user_data)
    except Exception as e:
        callback(error, text, e, user_data)


def on_result(req, result, data):
    error = data['error']
    user_data = data['user_data']
    text = data['text']
    try:
        stream = req.send_finish(result)
        stream.read_bytes_async(40960, 100, None, on_read, data)
    except Exception as e:
        callback(error, text, e, user_data)


def lookup(text, success, error, user_data=None):
    try:
        url = api.get_config().build_url(text)
        msg = Soup.Message.new('GET', url)
        log.debug('GET - %s' % url)
        headers = Soup.MessageHeaders.new(Soup.MessageHeadersType.REQUEST)
        for key, value in api.get_config().build_headers().items():
            msg.request_headers.append(key, value)
            log.debug('header - %s: %s' % (key, value))
        try:
            SESSION.props.proxy_uri = Soup.URI.new(config.PROXY_URI)
            log.debug('proxy %s' % config.PROXY_URI)
        except Exception as e:
            log.debug(
                '%s' % 'no proxy' if not config.PROXY_URI else 'invalid proxy %s' % config.PROXY_URI)
            SESSION.props.proxy_uri = None
        SESSION.send_async(msg, None, on_result,
                           {'success': success, 'error': error,
                            'text': text, 'user_data': user_data})
    except Exception as e:
        callback(error, text, e, user_data)
