#!/usr/bin/env python3
# encoding=utf8

from pydict.window import *

if __name__ != '__main__':
    raise Exception('cannot import %s as module' % __file__)


window = DictWindow()
Gtk.main()
