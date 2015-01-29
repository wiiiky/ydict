#coding=utf8


from gi.repository import Gtk
from query import youdao_query


class MainWindow(Gtk.Window):

    DEFAULT_WIDTH = 340
    DEFAULT_HEIGHT = 160

    """The Main Window of YouDao Dict"""

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        super().__init__()
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event",Gtk.main_quit)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        self.add(vbox)

        vbox.pack_start(self.create_menu_bar(),False,True,0)
        vbox.pack_start(self.create_content(),True,True,0)


        self.querying=""

        self.show_all()

        self.spinner.hide()

    def create_menu_bar(self):
        menubar = Gtk.MenuBar()

        _about=Gtk.MenuItem.new_with_mnemonic("_About")
        menubar.append(_about)

        about_menu = Gtk.Menu()
        _about.set_submenu(about_menu)

        about = Gtk.MenuItem("About")
        about_menu.append(about)

        return menubar

    def create_content(self):
        """docstring for create_content"""
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL,8)
        vbox.set_border_width(10)
        vbox.pack_start(self.create_query_box(),False,True,0)
        vbox.pack_start(self.create_result_box(),True,True,0)
        return vbox


    def create_query_box(self):
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10)
        self.entry = Gtk.Entry()
        self.entry.set_name("query_entry")
        self.entry.connect("activate",self.on_activate)
        hbox.pack_start(self.entry,True,True,0)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        hbox.pack_start(self.spinner,False,False,0)

        self.query = Gtk.Button.new_with_label("Query")
        self.query.set_name("query_button")
        self.query.connect("clicked",self.on_query)
        hbox.pack_start(self.query,False,False,0)
        return hbox


    def create_result_box(self):
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 15)

        # basic
        self.basic_expander = Gtk.Expander.new("")
        label = Gtk.Label.new("Basic")
        label.set_name("basic_expander_label")
        self.basic_expander.set_label_widget(label)
        vbox.pack_start(self.basic_expander,False,True,0)

        self.basic_result = Gtk.Label.new("")
        self.basic_result.set_halign(Gtk.Align.START)
        self.basic_result.set_margin_start(20)
        self.basic_result.set_name("basic_result_label")
        self.basic_expander.add(self.basic_result)

        # web
        self.web_expander = Gtk.Expander.new("")
        label = Gtk.Label.new("Web")
        label.set_name("web_expander_label")
        self.web_expander.set_label_widget(label)
        vbox.pack_start(self.web_expander,False,True,0)

        self.web_result = Gtk.Label.new("")
        self.web_result.set_halign(Gtk.Align.START)
        self.web_result.set_margin_start(20)
        self.web_result.set_name("web_result_label")
        self.web_expander.add(self.web_result)

        return vbox


    def on_activate(self,data):
        self.query.clicked()
        self.query.grab_focus()


    def on_query(self,data):
        text = self.entry.get_text()
        if not text:
            return
        self.querying = text
        self.spinner.show()
        youdao_query(text,self.on_success,self.on_error,self)


    def on_success(self,text,data):
        if text != self.querying:
            return

        basic_result = ""
        for basic in data["basic"]["explains"]:
            basic_result += basic + "\n"
        self.basic_result.set_text(basic_result)
        self.basic_expander.set_expanded(True)
        self.basic_result.show()

        web_result = ""
        for web in data["web"]:
            key = web["key"]
            value = web["value"]
            web_result += "%s\t\t%s\n" % (key, value)
        self.web_result.set_text(web_result)
        self.web_result.show()

        self.entry.grab_focus()
        self.entry.select_region(0,-1)
        self.spinner.hide()

    def on_error(self,text,e):
        self.spinner.hide()
        print(text,e)
