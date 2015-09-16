#!/usr/bin/env python3
# encoding=utf8


if __name__ != '__main__':
    raise Exception('cannot import %s as module' % __file__)

try:
    # 测试需要的模块是否存在
    from pydict.base import data as base
except:
    # 否则试图从当前目录导入
    import os
    import sys
    sys.path.append(os.path.curdir)

from pydict.window import *

window = DictWindow()
Gtk.main()
