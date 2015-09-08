# encoding=utf8
# 设置界面


from gi.repository import Gtk
from . import api
import pkgutil
import os


def list_services():
    """
    列出所有接口模块信息
    """
    services = []
    for loader, module_name, is_pkg in\
            pkgutil.walk_packages(os.path.dirname(__file__)):
        if not is_pkg:
            continue

        mod = loader.find_module(module_name).load_module(module_name)
        try:
            if mod.DICT_INFO and mod.DICT_INFO['enable']:
                info = dict(mod.DICT_INFO)
                info['module_name'] = module_name

                def set_default(d, name, default):
                    if name not in d:
                        d[name] = default

                set_default(info, 'description', 'no description')

                config_name = '%s.config' % module_name
                config = pkgutil.find_loader(
                    config_name).load_module(config_name)
                info['options'] = config.Config.get_options()
                info['current'] = config.Config.get_option()
                services.append(info)
                print(info)
        except Exception as e:
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

        # 接口列表
        renderer = Gtk.CellRendererToggle.new()
        renderer.connect("toggled", self._cell_toggled)
        renderer.set_radio(True)
        tree.append_column(Gtk.TreeViewColumn('Enable', renderer, active=0))
        renderer = Gtk.CellRendererText.new()
        tree.append_column(Gtk.TreeViewColumn('Dict', renderer, text=1))
        tree.append_column(Gtk.TreeViewColumn('Description', renderer, text=2))
        renderer = Gtk.CellRendererCombo.new()
        renderer.set_property("editable", True)
        renderer.set_property("text-column", 0)
        renderer.set_property("has-entry", False)
        renderer.connect("edited", self._on_option_changed)
        tree.append_column(Gtk.TreeViewColumn('Options', renderer,
                                              model=3, text=4))

        store = Gtk.ListStore(bool, str, str, Gtk.TreeModel, str, str)
        self.services = list_services()
        for service in self.services:
            enable = False
            if api.API == service['module_name']:
                enable = True
            options = Gtk.ListStore(str, object)
            for name, func in service['options'].items():
                options.append([name, func])
            store.append([enable,
                          service['name'],
                          service['description'],
                          options,
                          service['current'],
                          service['module_name']])
        tree.set_model(store)

        self.store = store
        content.show_all()

    def _on_option_changed(self, widget, path, text):
        self.store[path][4] = text

    def _cell_toggled(self, renderer, path):
        if self.store[path][0]:
            return
        for row in self.store:
            row[0] = False
        self.store[path][0] = True

    def _response(self, widget, ID, *args):
        if ID == Gtk.ResponseType.OK:
            self._save()
        self.destroy()

    def _save(self):
        """保存配置"""
        for row in self.store:
            if row[0]:
                api.API = row[-1]
                options = row[3]
                selected = row[4]
                for opt in options:
                    if opt[0] == selected:
                        opt[1]()
                        print('[DEBUG]', 'option %s' % selected)
                        break
                print('[DEBUG]', 'change API service to %s' % api.API)
                break
