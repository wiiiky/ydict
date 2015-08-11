# encoding=utf8


from gi.repository import Gtk, Gdk, Pango
from pydict.http import lookup
from pydict.about import AboutDialog


class DictWindow(Gtk.Window):

    DEFAULT_WIDTH = 480
    DEFAULT_HEIGHT = 320

    INSTANCE_COUNT = 0

    """词典的主界面"""

    def __init__(self, position=Gtk.WindowPosition.CENTER):
        super(DictWindow, self).__init__()
        self.set_title('Y')
        self.set_default_size(
            DictWindow.DEFAULT_WIDTH, DictWindow.DEFAULT_HEIGHT)
        self.set_position(position)
        self.connect('delete-event', self._quit)

        self.accelerators = Gtk.AccelGroup()
        self.add_accel_group(self.accelerators)
        # 创建主布局
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.add(vbox)
        vbox.pack_start(self._create_menu(), False, True, 0)
        vbox.pack_start(self._create_main(), True, True, 0)

        self.show_all()

        DictWindow.INSTANCE_COUNT += 1

    def destroy(self):
        super(DictWindow, self).destroy()
        DictWindow.INSTANCE_COUNT -= 1

    def _add_accel(self, widget, accelerator, signal):
        key, mod = Gtk.accelerator_parse(accelerator)
        widget.add_accelerator(
            signal, self.accelerators, key, mod, Gtk.AccelFlags.VISIBLE)

    def _menu_item_with_accel(self, label, accelerator, handler=None):
        item = Gtk.MenuItem.new_with_label(label)
        if handler:
            item.connect('activate', handler)
        self._add_accel(item, accelerator, 'activate')
        return item

    def _create_menu(self):
        """创建菜单"""
        bar = Gtk.MenuBar()

        item = Gtk.MenuItem.new_with_mnemonic('_File')
        bar.append(item)

        menu = Gtk.Menu()
        item.set_submenu(menu)

        item = self._menu_item_with_accel('New', '<Control>n', self._new)
        menu.append(item)
        item = self._menu_item_with_accel('Quit', '<Control>q', self._quit)
        menu.append(item)

        item = Gtk.MenuItem.new_with_mnemonic('_Help')
        bar.append(item)
        menu = Gtk.Menu()
        item.set_submenu(menu)

        item = self._menu_item_with_accel(
            'About', '<Control><Shift>a', self._about)
        menu.append(item)

        return bar

    def _create_main(self):
        """创建主要内容"""
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        vbox.set_margin_top(8)
        vbox.set_margin_right(8)
        vbox.set_margin_left(8)

        vbox.pack_start(self._create_entry(), False, True, 0)
        vbox.pack_start(self._create_textview(), True, True, 0)
        vbox.pack_start(self._create_status_bar(), False, False, 0)
        return vbox

    def _create_entry(self):
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 15)
        self.entry = Gtk.Entry.new()
        self.entry.connect('activate', self._lookup)
        hbox.pack_start(self.entry, True, True, 0)
        self.lookup = Gtk.Button.new_with_label('Look up')
        self.lookup.connect('clicked', self._lookup)
        hbox.pack_start(self.lookup, False, True, 0)
        return hbox

    def _create_textview(self):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        text_buffer = self.textview.get_buffer()
        text_buffer.create_tag(
            'title', size_points=20, weight=Pango.Weight.BOLD, style=Pango.Style.ITALIC, foreground='#000000')
        text_buffer.create_tag(
            'phonetic', size_points=12, style=Pango.Style.ITALIC,
                               foreground="#666666")
        text_buffer.create_tag(
            'basic_title', size_points=15, weight=Pango.Weight.BOLD,
                               foreground='#000000')
        text_buffer.create_tag('basic', size_points=12, foreground='#000000')
        text_buffer.create_tag('extra_key', size_points=12,
                               foreground='#1111ff', style=Pango.Style.ITALIC)
        scrolled_window.add(self.textview)

        return scrolled_window

    def _create_status_bar(self):
        self.statusbar = Gtk.Statusbar()
        return self.statusbar

    def _new(self, widget):
        win = DictWindow(position=Gtk.WindowPosition.NONE)

    def _quit(self, *args):
        self.destroy()
        if DictWindow.INSTANCE_COUNT <= 0:
            Gtk.main_quit()

    def _about(self, widget):
        dialog = AboutDialog(self)
        dialog.show()

    def _lookup(self, widget):
        text = self.entry.get_text()
        if not text:
            return
        self.statusbar.remove_all(1)
        self.statusbar.push(1, 'Searching for \'%s\'' % text)
        lookup(text, self._on_success, self._on_error)

    def _on_success(self, text, data):
        if data.has_error():
            self.statusbar.push(1, 'errorCode: %s' % data.errorCode)
            return
        self.statusbar.push(1, 'A definition found')
        text_buffer = self.textview.get_buffer()
        text_buffer.set_text('', -1)
        text_buffer.insert_with_tags_by_name(
            text_buffer.get_end_iter(), '  %s ' % data.get_title(), 'title')
        text_buffer.insert_with_tags_by_name(
            text_buffer.get_end_iter(), '%s\n' % data.get_phonetic(), 'phonetic')
        text_buffer.insert_with_tags_by_name(
            text_buffer.get_end_iter(), 'Basic:\n', 'basic_title')
        for basic in data.get_basic():
            text_buffer.insert_with_tags_by_name(
                text_buffer.get_end_iter(), '\t%s\n' % basic, 'basic')
        extra = data.get_extra()
        if not extra:
            return
        text_buffer.insert_with_tags_by_name(
            text_buffer.get_end_iter(), 'Extra:\n', 'basic_title')
        for ex in extra:
            text_buffer.insert_with_tags_by_name(
                text_buffer.get_end_iter(), '\t%s: ' % ex['key'], 'extra_key')
            text_buffer.insert_with_tags_by_name(
                text_buffer.get_end_iter(), '%s\n' % ex['value'], 'basic')

    def _on_error(self, text, e):
        self.statusbar.push(1, 'error: %s' % str(e))
