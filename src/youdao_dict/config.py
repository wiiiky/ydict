# coding=utf8

#
# config.py
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

from gi.repository import GLib


gConfigDir = GLib.get_user_config_dir() + "/youdao_dict"

gConfigFile = gConfigDir + '/conf'


class Config:

    GROUP = "ydict"
    HYPER_TRANSLATE = "HyperTanslate"

    def __init__(self):
        self.keyfile = GLib.KeyFile.new()
        self.hypertanslate = False
        try:
            self.keyfile.load_from_file(gConfigFile, GLib.KeyFileFlags.NONE)
            self.hypertanslate = self.keyfile.get_boolean(Config.GROUP,
                                                          Config.HYPER_TRANSLATE)
        except:
            pass

    def is_hypertranslate(self):
        return self.hypertanslate

    def set_hypertranslate(self, b):
        self.hypertanslate = b
        self.keyfile.set_boolean(Config.GROUP, Config.HYPER_TRANSLATE, b)
        self.keyfile.save_to_file(gConfigFile)

gConfig = Config()
