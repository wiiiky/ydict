# encoding=utf8
# 设置的窗口


from gi.repository import Gtk


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

    def _response(self, widget, ID, *args):
        self.destroy()
