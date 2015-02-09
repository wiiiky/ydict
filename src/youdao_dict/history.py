# coding=utf8

#
# history.py
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


import os
import sqlite3
import time
from gi.repository import GLib
from youdao_dict.config import gConfigDir

gSQLite3Path = gConfigDir + "/history.sqlite3"

HISTORY_TABLE = 'query_history'
HISTORY_COL_TEXT = 'text'
HISTORY_COL_BASIC = 'basic'
HISTORY_COL_TIME = 'time'

try:
    os.mkdir(gConfigDir)
except:
    pass

gSQLite3Connection = sqlite3.connect(gSQLite3Path)

try:
    cur = gSQLite3Connection.cursor()
    cur.execute('create table %s '
                '(id integer not null primary key autoincrement,'
                '%s varchar(100) not null,'
                '%s varchar(100) not null,'
                '%s integer not null)'
                % (HISTORY_TABLE, HISTORY_COL_TEXT, HISTORY_COL_BASIC, HISTORY_COL_TIME))
    gSQLite3Connection.commit()
    cur.close()
except sqlite3.OperationalError:
    pass


def record(text, basic=''):
    global gSQLite3Connection

    cur = gSQLite3Connection.cursor()
    statement = 'insert into %s(%s,%s,%s) values(?,?,?)'\
        % (HISTORY_TABLE, HISTORY_COL_TEXT, HISTORY_COL_BASIC, HISTORY_COL_TIME)
    cur.execute(statement, (text, basic, int(time.time())))
    gSQLite3Connection.commit()
    cur.close()


def clear_all():
    global gSQLite3Connection

    cur = gSQLite3Connection.cursor()
    statement = 'delete from %s' % HISTORY_TABLE
    cur.execute(statement)
    gSQLite3Connection.commit()
    cur.close()


def get_history(n=100):
    try:
        cur = gSQLite3Connection.cursor()
        statement = 'select %s from %s group by text '\
            'order by id desc limit %s' % (HISTORY_COL_TEXT, HISTORY_TABLE, n)
        cur.execute(statement)
        texts = cur.fetchall()
        history = []
        for text in texts:
            history.append(text[0])
        cur.close()
        return history
    except Exception as e:
        print(e)
        return []
