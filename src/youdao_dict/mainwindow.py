# coding=utf8

#
# mainwindow.py
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
from gi.repository import GObject
from youdao_dict.query import youdao_query
from youdao_dict.i18n import _
from youdao_dict.aboutdialog import AboutDialog
from youdao_dict.history import record, get_history, clear_all
from youdao_dict.clipboard import start_listen, stop_listen


class MainWindow(Gtk.Window):

    DEFAULT_WIDTH = 340
    DEFAULT_HEIGHT = 160

    """The Main Window of YouDao Dict"""

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        super(MainWindow, self).__init__()

        self.set_title(_("Y"))
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        self.add(vbox)

        vbox.pack_start(self.create_menu_bar(), False, True, 0)
        vbox.pack_start(self.create_content(), True, True, 0)

        self.querying = ""

        self.show_all()

        self.spinner.hide()
        self.basic_result.hide()
        self.web_result.hide()

        self.set_keep_above(True)

    def create_menu_bar(self):
        menubar = Gtk.MenuBar()

        setting = Gtk.MenuItem.new_with_mnemonic(_("_Setting"))
        menubar.append(setting)
        setting_menu = Gtk.Menu()
        setting.set_submenu(setting_menu)
        hyper_setting = Gtk.CheckMenuItem.new_with_mnemonic(
            _("_Hyper Translate"))
        hyper_setting.connect("toggled", self.on_hyper_toggled)
        setting_menu.append(hyper_setting)

        clear_setting = Gtk.MenuItem.new_with_mnemonic(_("Clear History"))
        clear_setting.connect("activate", self.on_clear_history)
        setting_menu.append(clear_setting)

        _about = Gtk.MenuItem.new_with_mnemonic(_("_About"))
        menubar.append(_about)
        about_menu = Gtk.Menu()
        _about.set_submenu(about_menu)
        about = Gtk.MenuItem(_("About"))
        about.connect("activate", self.on_about_item)
        about_menu.append(about)

        return menubar

    def create_content(self):
        """docstring for create_content"""
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 8)
        vbox.set_border_width(10)
        vbox.pack_start(self.create_query_box(), False, True, 0)
        vbox.pack_start(self.create_result_box(), True, True, 0)
        return vbox

    def create_query_box(self):
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10)
        self.entry = Gtk.Entry()
        self.entry.set_name("query_entry")
        self.entry.connect("activate", self.on_activate)
        hbox.pack_start(self.entry, True, True, 0)

        # sets GtkEntryCompletion
        self.completion = Gtk.EntryCompletion.new()
        self.completion.set_text_column(0)
        self.history = get_history()
        self.model = Gtk.ListStore.new([GObject.TYPE_STRING])
        for text in self.history:
            it = self.model.append()
            self.model.set(it, [0], [text])
        self.completion.set_model(self.model)
        self.entry.set_completion(self.completion)

        # spinner
        self.spinner = Gtk.Spinner()
        self.spinner.start()
        hbox.pack_start(self.spinner, False, False, 0)

        self.query = Gtk.Button.new_with_label(_("Query"))
        self.query.set_name("query_button")
        self.query.connect("clicked", self.on_query_button)
        hbox.pack_start(self.query, False, False, 0)
        return hbox

    def create_result_box(self):
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 15)

        # basic
        self.basic_expander = Gtk.Expander.new("")
        label = Gtk.Label.new(_("Basic"))
        label.set_name("basic_expander_label")
        self.basic_expander.set_label_widget(label)
        vbox.pack_start(self.basic_expander, False, True, 0)

        self.basic_result = Gtk.Label.new("")
        self.basic_result.set_halign(Gtk.Align.START)
        self.basic_result.set_margin_start(20)
        self.basic_result.set_name("basic_result_label")
        self.basic_expander.add(self.basic_result)

        # web
        self.web_expander = Gtk.Expander.new("")
        label = Gtk.Label.new(_("Web"))
        label.set_name("web_expander_label")
        self.web_expander.set_label_widget(label)
        vbox.pack_start(self.web_expander, False, True, 0)

        self.web_result = Gtk.Label.new("")
        self.web_result.set_halign(Gtk.Align.START)
        self.web_result.set_margin_start(20)
        self.web_result.set_name("web_result_label")
        self.web_expander.add(self.web_result)

        return vbox

    def on_hyper_toggled(self, item):
        if item.get_active():
            start_listen(self.on_clipboard_text)
        else:
            stop_listen()

    def on_clear_history(self, item):
        clear_all()
        self.history = []
        self.model.clear()

    def on_clipboard_text(self, text):
        if not text:
            return
        self.start_query(text)

    def on_about_item(self, item):
        AboutDialog(self).show()

    def on_activate(self, entry):
        self.query.clicked()
        self.query.grab_focus()

    def on_query_button(self, button):
        text = self.entry.get_text()
        if not text:
            return
        self.start_query(text)

    def start_query(self, text):
        self.querying = text
        self.spinner.show()
        self.entry.set_text(text)
        youdao_query(text, self.on_success, self.on_error, self)

    def on_success(self, text, data):
        if text != self.querying:
            return

        if "basic" in data:     # replace in operator with has_key in python3
            basic_result = ""
            if "phonetic" in data["basic"]:
                basic_result += "[ " + data["basic"]["phonetic"] + " ]\n"
            for basic in data["basic"]["explains"]:
                basic_result += basic + "\n"
            self.basic_result.set_text(basic_result)
            self.basic_expander.set_expanded(True)
            self.basic_result.show()
            record(text, basic_result)
            if text not in self.history:
                it = self.model.prepend()
                self.model.set(it, [0], [text])
        else:
            self.basic_result.set_text("")
            self.basic_result.hide()

        web_result = ""
        if "web" in data:
            for web in data["web"]:
                key = web["key"]
                value = web["value"]
                web_result += "%s\t\t%s\n" % (key, value)
            self.web_result.set_text(web_result)
            self.web_expander.set_expanded(True)
            self.web_result.show()
        else:
            self.web_result.set_text("")
            self.web_result.hide()

        self.entry.grab_focus()
        self.entry.select_region(0, -1)
        self.spinner.hide()
        self.resize(1, 1)

    def on_error(self, text, e):
        self.spinner.hide()
        print(text, e)
