#!/usr/bin/python3

import gi
import os
from threadProgress import ThreadProgress

gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository import GObject

class Interface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self,title="Interface")
        self.connect("delete-event",Gtk.main_quit)
        self.set_default_size(550,320)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        #Darknet path
        self.path=""
        #Islenecek resim dosyasinin yolu
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


        ## Event Kismi ##

        self.vBoxevent=Gtk.VBox()
        self.fixed.put(self.vBoxevent,10,15)

        label=Gtk.Label()
        label.set_markup("<b>Output Image</b>")
        self.vBoxevent.pack_start(label,False,False,0)

        self.fixedevent=Gtk.Fixed()
        self.vBoxevent.pack_start(self.fixedevent,True,True,0)

        self.imageoutput=Gtk.Image()
        self.fixedevent.put(self.imageoutput,10,62)

        ## *** ##

        """ seperator gozukmuyor"""
        seperator2=Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.fixed.put(seperator2,240,15)

        self.vBoxview=Gtk.VBox(spacing=10)
        self.vBoxview.set_homogeneous(False)
        self.fixed.put(self.vBoxview,270,15)

        #self.label=Gtk.Label("Bellek CO.")
        #self.vBoxevent.pack_start(self.label,False,False,0)

        ## View kismi ##

        label=Gtk.Label()
        label.set_markup("<b>Please select the image file to be processed!</b>")
        self.vBoxview.pack_start(label,False,False,0)

        self.filechooserbutton=Gtk.FileChooserButton(title="İşlenecek resmi seçiniz!")
        self.filechooserbutton.set_action(0)
        self.filechooserbutton.connect("file-set",self.file_changed)
        self.filechooserbutton.set_width_chars(25)
        self.vBoxview.pack_start(self.filechooserbutton,True,True,0)

        seperator=Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.vBoxview.pack_start(seperator,False,False,0)

        self.imageinput=Gtk.Image()
        self.vBoxview.pack_start(self.imageinput,False,False,0)

        self.runbutton=Gtk.Button.new_with_label("Start Progress")
        self.vBoxview.pack_start(self.runbutton,False,False,0)
        self.runbutton.connect("clicked",self.on_click_run_button)

        self.spinner=Gtk.Spinner()
        self.vBoxview.pack_start(self.spinner,False,True,0)

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
            pixinput=GdkPixbuf.Pixbuf.new_from_file_at_size(self.filechooserbutton.get_filename(),250,400)
            self.imageinput.set_from_pixbuf(pixinput)
            self.choosenimage=filechooserdialog.get_filename()
        filechooserdialog.destroy()

    def on_click_run_button(self,widget):

        if self.choosenimage=="":
            errormessage=Gtk.MessageDialog(self,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,
                                           "Hata!")
            errormessage.format_secondary_text(
                "Lütfen işlenecek resmi seçiniz!"
            )
            errormessage.run()
            errormessage.destroy()
            return

        if self.path=="":
            filechooser=Gtk.FileChooserDialog(title="Darknet'in bulunduğu yolu seçiniz")
            filechooser.set_action(2)
            filechooser.add_button("_Open",Gtk.ResponseType.OK)
            filechooser.add_button("_Cancel",Gtk.ResponseType.CANCEL)
            filechooser.set_default_response(Gtk.ResponseType.OK)
            response=filechooser.run()

            if response == Gtk.ResponseType.OK :
                self.path=filechooser.get_filename()

            filechooser.destroy()

        command="./darknet detect cfg/yolo.cfg yolo.weights "+self.choosenimage

        progress=ThreadProgress(self.imageoutput,self.spinner,command,self.path)
        progress.start()

        self.spinner.start()
        self.vBoxview.show_all()


    def all_quit(self,widget):
        Gtk.main_quit()

    def file_changed(self,widget):
        pix=GdkPixbuf.Pixbuf.new_from_file_at_size(self.filechooserbutton.get_filename(),250,400)
        self.imageinput.set_from_pixbuf(pix)
        self.choosenimage=self.filechooserbutton.get_filename()


window=Interface()
window.show_all()
Gtk.main()
