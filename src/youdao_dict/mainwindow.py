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
from youdao_dict.query import youdao_query
from youdao_dict.i18n import _
from youdao_dict.aboutdialog import AboutDialog
from youdao_dict.history import record


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

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        hbox.pack_start(self.spinner, False, False, 0)

        self.query = Gtk.Button.new_with_label(_("Query"))
        self.query.set_name("query_button")
        self.query.connect("clicked", self.on_query)
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

    def on_about_item(self, item):
        AboutDialog(self).show()

    def on_activate(self, entry):
        self.query.clicked()
        self.query.grab_focus()

    def on_query(self, button):
        text = self.entry.get_text()
        if not text:
            return
        self.querying = text
        self.spinner.show()
        youdao_query(text, self.on_success, self.on_error, self)

    def on_success(self, text, data):
        if text != self.querying:
            return

        basic_result = ""
        if "basic" in data:     # replace in operator with has_key in python3
            for basic in data["basic"]["explains"]:
                basic_result += basic + "\n"
            self.basic_result.set_text(basic_result)
            self.basic_expander.set_expanded(True)
            self.basic_result.show()
            record(text, basic_result)
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
