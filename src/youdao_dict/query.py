# coding=utf8

#
# query.py
#
# Copyright (C) 2015 - Wiky L <wiiiky@outlook.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


from gi.repository import Soup
import json


gSession = Soup.Session()


class QueryData(object):

    """docstring for QueryData"""

    def __init__(self, text, success, error, user_data):
        self.text = text
        self.on_success = success
        self.on_error = error
        self.user_data = user_data


def on_read(inputstream, result, data):
    """docstring for on_read"""
    on_error = data.on_error
    on_success = data.on_success
    text = data.text
    user_data = data.user_data

    try:
        bytes = inputstream.read_bytes_finish(result)
        if bytes:
            data = str(bytes.get_data(), 'utf-8')
            jdata = json.loads(data)
            if jdata["errorCode"] == 0:
                on_success(text, jdata)
                return
    except Exception as e:
        on_error(text, e)


def on_query(req, result, data):
    """docstring for on_query"""
    on_error = data.on_error
    text = data.text
    user_data = data.user_data
    try:
        inputstream = req.send_finish(result)
        if inputstream:
            inputstream.read_bytes_async(40960, 100, None, on_read, data)
            return
    except Exception as e:
        on_error(text, e)


def youdao_query(text, success, error, user_data):
    """
    text - the string to query
    success - the callback when query successes. success(user_data,text,data)
    error - the callback on error.     error(user_data,text,Exception)
    """
    global gSession
    try:
        request = gSession.request(
            'http://fanyi.youdao.com/openapi.do?keyfrom=github-wdict&key=619541059&type=data&doctype=json&version=1.1&q=%s' % text)
        request.send_async(None, on_query,
                           QueryData(text, success, error, user_data))
    except Exception as e:
        error(text, e)
