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


gConfigDir = GLib.get_user_config_dir() + "/youdao_dict"
gSQLite3Path = gConfigDir + "/history.sqlite3"

SQLITE3_DB = 'query_history'
SQLITE3_COL_TEXT = 'text'
SQLITE3_COL_BASIC = 'basic'
SQLITE3_COL_TIME = 'time'

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
                % (SQLITE3_DB, SQLITE3_COL_TEXT, SQLITE3_COL_BASIC, SQLITE3_COL_TIME))
    gSQLite3Connection.commit()
    cur.close()
except sqlite3.OperationalError:
    pass


def record(text, basic=''):
    global gSQLite3Connection

    cur = gSQLite3Connection.cursor()
    statement = 'insert into %s(%s,%s,%s) values(?,?,?)'\
        % (SQLITE3_DB, SQLITE3_COL_TEXT, SQLITE3_COL_BASIC, SQLITE3_COL_TIME)
    cur.execute(statement, (text, basic, int(time.time())))
    gSQLite3Connection.commit()
    cur.close()
