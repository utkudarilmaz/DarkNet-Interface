#!/usr/bin/python3

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository import GObject

class Interface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self,title="Interface")
        self.connect("delete-event",Gtk.main_quit)
        self.set_default_size(510,320)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        self.choosenimage=""

        self.vBox=Gtk.VBox()
        self.add(self.vBox)

        self.menubar=Gtk.MenuBar()
        self.vBox.pack_start(self.menubar,False,False,0)
        self.menubar.set_hexpand(True)

        filemenu=Gtk.MenuItem(label="File")
        self.menubar.append(filemenu)

        menu=Gtk.Menu()
        filemenu.set_submenu(menu)

        filechoosermenu=Gtk.MenuItem(label="Choose Image")
        filechoosermenu.connect("activate",self.get_file_chooser_dialog)
        menu.append(filechoosermenu)

        quitmenu=Gtk.MenuItem(label="Quit (ALt+F4)")
        quitmenu.connect("activate",self.all_quit)
        menu.append(quitmenu)


        self.fixed=Gtk.Fixed()
        self.vBox.pack_start(self.fixed,True,True,0)

        self.vBoxevent=Gtk.VBox()
        self.fixed.put(self.vBoxevent,0,0)

        """ seperator gozukmuyor"""
        seperator2=Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.fixed.put(seperator2,160,15)

        self.vBoxview=Gtk.VBox(spacing=10)
        self.vBoxview.set_homogeneous(False)
        self.fixed.put(self.vBoxview,250,15)

        self.label=Gtk.Label("Bellek CO.")
        self.vBoxevent.pack_start(self.label,False,False,0)

        ## View kismi ##

        label=Gtk.Label()
        label.set_markup("<b>Lütfen işlenecek resim dosyasını seçiniz!</b>")
        self.vBoxview.pack_start(label,False,False,0)

        self.filechooserbutton=Gtk.FileChooserButton(title="İşlenecek resmi seçiniz!")
        self.filechooserbutton.set_action(0)
        self.filechooserbutton.connect("file-set",self.file_changed)
        self.filechooserbutton.set_width_chars(25)
        self.vBoxview.pack_start(self.filechooserbutton,True,True,0)

        seperator=Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.vBoxview.pack_start(seperator,False,False,0)

        self.image=Gtk.Image()
        self.pix=None
        self.vBoxview.pack_start(self.image,False,False,0)

        self.runbutton=Gtk.Button.new_with_label("Start Progress")
        self.vBoxview.pack_start(self.runbutton,False,False,0)
        self.runbutton.connect("clicked",self.on_click_run_button)

        ## *** ##

    def get_file_chooser_dialog(self,widget):
        filechooserdialog=Gtk.FileChooserDialog(title="İşlenecek resmi seçiniz!")
        filechooserdialog.set_action(0)
        filechooserdialog.add_button("_Open",Gtk.ResponseType.OK)
        filechooserdialog.add_button("_Cancel",Gtk.ResponseType.CANCEL)
        filechooserdialog.set_default_response(Gtk.ResponseType.OK)
        response=filechooserdialog.run()
        if response == Gtk.ResponseType.OK :
            self.filechooserbutton.set_filename(filechooserdialog.get_filename())
            self.pix=GdkPixbuf.Pixbuf.new_from_file_at_size(self.filechooserbutton.get_filename(),250,400)
            self.image.set_from_pixbuf(self.pix)
            self.choosenimage=filechooserdialog.get_filename()
        filechooserdialog.destroy()

    def on_click_run_button(self,widget):
        pass

    def all_quit(self,widget):
        Gtk.main_quit()

    def file_changed(self,widget):
        self.pix=GdkPixbuf.Pixbuf.new_from_file_at_size(self.filechooserbutton.get_filename(),250,400)
        self.image.set_from_pixbuf(self.pix)
        self.choosenimage=self.filechooserbutton.get_filename()


window=Interface()
window.show_all()
Gtk.main()
