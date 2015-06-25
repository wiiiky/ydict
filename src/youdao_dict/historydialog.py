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
from gi.repository import Gtk, Pango
from youdao_dict.i18n import _
from youdao_dict.history import get_history_text


class HistoryDialog(Gtk.Dialog):

    """docstring for HistoryDialog"""

    def __init__(self, parent):
        super(HistoryDialog, self).__init__(parent=parent)
        self.main_window = parent
        self.set_title(_('Query History'))
        self.set_default_size(360, 480)
        self.connect("response", self.response_handler)

        scrolledWindow = Gtk.ScrolledWindow.new()
        view = Gtk.TreeView.new()
        view.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        view.set_enable_search(False)
        view.connect('row-activated', self.on_phrase_selected)
        scrolledWindow.add(view)

        cell = Gtk.CellRendererText.new()
        cell.set_property('ellipsize', Pango.EllipsizeMode.END)
        col = Gtk.TreeViewColumn(_('Phrase'),cell, text=0)
        view.append_column(col)

        # cell = Gtk.CellRendererText.new()
        # cell.set_property('ellipsize', Pango.EllipsizeMode.END)
        # col = Gtk.TreeViewColumn(_('Definition'), cell, text=1)
        # view.append_column(col)

        history = get_history_text()
        model = Gtk.ListStore(str, str)
        for phrase, definition in history:
            model.append([str(phrase), str(definition)])
        view.set_model(model)

        self.get_content_area().pack_start(scrolledWindow, True, True, 0)
        self.get_action_area().set_margin_top(10)
        self.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

        self.show_all()

    def response_handler(self, dialog, response_id):
        if response_id == Gtk.ResponseType.DELETE_EVENT or\
                response_id == Gtk.ResponseType.CLOSE:
            self.hide()
            self.destroy()

    def on_phrase_selected(self, tree, path, column):
        model = tree.get_model()
        it = model.get_iter(path)
        if it:
            phrase = model.get(it,0)[0]
            self.main_window.start_query(phrase)
            self.destroy()
