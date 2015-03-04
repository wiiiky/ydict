# coding=utf8

#
# aboutdialog.py
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

import time
from gi.repository import Gtk
from youdao_dict.history import get_history_text


class HistoryDialog(Gtk.Dialog):

    """docstring for HistoryDialog"""

    def __init__(self, parent):
        super(HistoryDialog, self).__init__(parent=parent)
        self.set_border_width(10)
        self.set_default_size(360, 480)
        self.connect("response", self.response_handler)

        view = Gtk.TreeView.new()

        col = Gtk.TreeViewColumn("Time",
                                 Gtk.CellRendererText.new(), text=0)
        view.append_column(col)

        col = Gtk.TreeViewColumn("Text",
                                 Gtk.CellRendererText.new(), text=1)
        view.append_column(col)

        history = get_history_text()
        model = Gtk.ListStore(str, str)
        for text, t in history:
            model.append([time.ctime(t)[4:-5], str(text)])
        view.set_model(model)

        self.get_content_area().pack_start(view, True, True, 0)
        self.get_action_area().set_margin_top(10)
        self.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

        self.show_all()

    def response_handler(self, dialog, response_id):
        if response_id == Gtk.ResponseType.DELETE_EVENT or\
                response_id == Gtk.ResponseType.CLOSE:
            self.hide()
            self.destroy()
