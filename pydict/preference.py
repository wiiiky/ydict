# encoding=utf8
# 设置的窗口


from gi.repository import Gtk
import importlib
import pkgutil
import os


def list_services():
    services = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(os.path.dirname(__file__)):
        if is_pkg:
            mod = loader.find_module(module_name).load_module(module_name)
            try:
                if mod.DICT_SERVICE:
                    services.append({'name': module_name,
                                     'description': mod.DICT_DESCRIPTION})
            except:
                pass
    return services


class PreferenceDialog (Gtk.Dialog):

    DEFAULT_WIDTH = 400
    DEFAULT_HEIGHT = 280

    def __init__(self, parent):
        super(PreferenceDialog, self).__init__(
            title='Preference', parent=parent)
        self.set_default_size(
            PreferenceDialog.DEFAULT_WIDTH, PreferenceDialog.DEFAULT_HEIGHT)
        self.set_modal(True)
        self.set_border_width(10)
        self.add_buttons(
            "Save", Gtk.ResponseType.OK, "Close", Gtk.ResponseType.CLOSE)
        self.connect('response', self._response)
        self._init_content()

    def _init_content(self):
        """初始化界面元素"""
        content = self.get_content_area()
        main = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        main.set_margin_bottom(15)
        content.pack_start(main, True, True, 0)
        switcher = Gtk.StackSwitcher.new()
        main.pack_start(switcher, False, False, 0)
        stack = Gtk.Stack.new()
        main.pack_start(stack, True, True, 0)
        switcher.set_stack(stack)
        tree = Gtk.TreeView.new()
        stack.add_titled(tree, 'dict', 'Source')
        print(list_services())

        content.show_all()

    def _response(self, widget, ID, *args):
        if ID == Gtk.ResponseType.OK:
            print('ok')
        else:
            print('ID =', ID)
        self.destroy()
