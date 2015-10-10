# encoding=utf-8

from gi.repository import Gtk
from .i18n import _


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        super(AboutDialog, self).__init__(title=_('About'), parent=parent)
        self.set_modal(True)
        self.set_program_name('Ydict')
        self.set_authors(['Wiky L<wiiiky@outlook.com>'])
        self.set_artists(['Wiky L<wiiiky@outlook.com>'])
        self.set_comments('')
        self.set_copyright('Copyright (c) Wiky L 2015')
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_logo_icon_name('ydict')
        self.set_version('1.0')
        self.set_website('https://github.com/wiiiky/ydict')
        self.set_website_label('GitHub')
        self.set_wrap_license(True)
