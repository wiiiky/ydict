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


from gi.repository import Gtk
from youdao_dict.local import _


class AboutDialog(Gtk.AboutDialog):

    """docstring for AboutDialog"""

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(
            parent=parent, title=_("About YDict"))

        self.set_program_name(_("ydict"))
        self.set_version("0.1")
        self.set_logo_icon_name("gnome-terminal")
        self.set_copyright("Copyright (C) 2015 Wiky L")
        self.set_authors(["Wiky L <wiiiky@outlook.com>"])
        self.set_artists(["Wiky L <wiiiky@outlook.com>"])
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_wrap_license(True)
        self.set_website("https://github.com/wiiiky/ydict")
        self.set_translator_credits(_("translator-credits"))
