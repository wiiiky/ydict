# coding=utf8

#
# clipboard.py
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


from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib


TIMEER = None
LAST_TEXT = None


def get_clipboard_text():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    text = clipboard.wait_for_text()
    return text


def clear_clipboard():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    clipboard.set_text('', 0)


def timeout_callback(data):
    global LAST_TEXT
    text = get_clipboard_text()
    if text and LAST_TEXT != text:
        callback = data['callback']
        LAST_TEXT = text
        callback(text)
    return True


def start_listen(callback):
    global TIMEER, LAST_TEXT
    stop_listen()
    TIMEER = GLib.timeout_add(250, timeout_callback, {'callback': callback})


def stop_listen():
    global TIMEER, LAST_TEXT
    if TIMEER:
        GLib.source_remove(TIMEER)
        TIMEER = None
    LAST_TEXT = None
    clear_clipboard()
