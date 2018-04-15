#!/usr/bin/python3

import os
from threadProgress import ThreadProgress

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository import GObject

class Interface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self,title="Interface")
        self.connect("delete-event",Gtk.main_quit)
        self.set_default_size(1024,768)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        #Darknet path
        self.path=""
        #Islenecek resim dosyasinin yolu
        self.choosenimage=""

        self.grid=Gtk.Grid()
        self.add(self.grid)

        ## Menu ##

        self.menubar=Gtk.MenuBar()
        self.grid.attach(self.menubar,0,0,100,10)
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

        ## *** ##

        ## Event Kismi ##

        self.vBoxevent=Gtk.VBox()
        self.grid.attach(self.vBoxevent,1,10,84,60)

        label=Gtk.Label()
        label.set_markup("<big><b>Output Image</b></big>")
        self.vBoxevent.pack_start(label,False,False,5)

        self.imageoutput=Gtk.Image()
        self.vBoxevent.pack_start(self.imageoutput,True,True,25)
        pix=GdkPixbuf.Pixbuf.new_from_file_at_size("../images/blank.jpg",550,700)
        self.imageoutput.set_from_pixbuf(pix)

        ## *** ##

        seperator=Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.grid.attach(seperator,86,10,1,84)


        ## View kismi ##

        self.vBoxview=Gtk.VBox(spacing=10)
        self.vBoxview.set_homogeneous(False)
        self.grid.attach(self.vBoxview,88,10,11,85)
        #self.fixed.put(self.vBoxview,740,15)

        label=Gtk.Label()
        label.set_markup("<b>Please select the image file to be processed!</b>")
        self.vBoxview.pack_start(label,False,False,0)

        self.filechooserbutton=Gtk.FileChooserButton(title="İşlenecek resmi seçiniz!")
        self.filechooserbutton.set_action(0)
        self.filechooserbutton.connect("file-set",self.file_changed)
        self.filechooserbutton.set_width_chars(15)
        self.vBoxview.pack_start(self.filechooserbutton,False,False,0)

        seperator=Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.vBoxview.pack_start(seperator,False,False,0)

        self.imageinput=Gtk.Image()
        self.vBoxview.pack_start(self.imageinput,False,False,0)
        pix=GdkPixbuf.Pixbuf.new_from_file_at_size("../images/blank.jpg",250,400)
        self.imageinput.set_from_pixbuf(pix)

        self.runbutton=Gtk.Button.new_with_label("Start Progress")
        fixedRunButton=Gtk.Fixed()
        self.vBoxview.pack_start(fixedRunButton,True,True,0)
        fixedRunButton.put(self.runbutton,100,450)
        #self.vBoxview.pack_start(self.runbutton,True,True,0)
        self.runbutton.connect("clicked",self.on_click_run_button)

        ## *** ##

        seperator=Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid.attach(seperator,0,81,86,1)

        ## Log Kismi ##

        self.logBox=Gtk.VBox()
        self.grid.attach(self.logBox,0,82,86,12)

        logToolbar=Gtk.Toolbar()
        self.logBox.pack_start(logToolbar,False,False,0)

        logClearButton=Gtk.ToolButton()
        logClearButton.set_icon_name("edit-clear-symbolic")
        logClearButton.connect("clicked",self.on_log_clear_button)
        logToolbar.insert(logClearButton,0)

        logSearchButton=Gtk.ToolButton()
        logSearchButton.set_icon_name("system-search-symbolic")
        logToolbar.insert(logSearchButton,1)

        self.logScrolledWindow=Gtk.ScrolledWindow()
        self.logScrolledWindow.set_hexpand(True)
        self.logScrolledWindow.set_vexpand(True)
        self.logBox.pack_start(self.logScrolledWindow,True,True,0)

        self.textView=Gtk.TextView()
        self.textView.set_editable(False)
        self.textView.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textView.set_cursor_visible(False)
        self.logScrolledWindow.add(self.textView)

        self.textBuffer=self.textView.get_buffer()

        ## *** ##

        seperator=Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid.attach(seperator,0,94,100,1)

        ## Status Bar ##

        self.statusBar=Gtk.HBox()
        self.grid.attach(self.statusBar,0,95,100,5)

        self.spinner=Gtk.Spinner()
        self.statusBar.pack_start(self.spinner,True,True,0)

        ## ** ##

    def get_file_chooser_dialog(self,widget):
        filechooserdialog=Gtk.FileChooserDialog(title="İşlenecek resmi seçiniz!")
        filechooserdialog.set_action(0)
        filechooserdialog.add_button("_Open",Gtk.ResponseType.OK)
        filechooserdialog.add_button("_Cancel",Gtk.ResponseType.CANCEL)
        filechooserdialog.set_default_response(Gtk.ResponseType.OK)
        response=filechooserdialog.run()
        if response == Gtk.ResponseType.OK :
            self.filechooserbutton.set_filename(filechooserdialog.get_filename())
            pixinput=GdkPixbuf.Pixbuf.new_from_file_at_size(self.filechooserbutton.get_filename(),275,425)
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

        if self.path=="" :
            return

        command="./darknet detect cfg/yolo.cfg yolo.weights "+self.choosenimage

        progress=ThreadProgress(self.imageoutput,self.spinner,command,self.path)
        progress.start()

        self.spinner.start()
        self.vBoxview.show_all()

    def all_quit(self,widget):
        Gtk.main_quit()

    def file_changed(self,widget):
        pix=GdkPixbuf.Pixbuf.new_from_file_at_size(self.filechooserbutton.get_filename(),275,425)
        self.imageinput.set_from_pixbuf(pix)
        self.choosenimage=self.filechooserbutton.get_filename()

    def on_log_clear_button(self,widget):
        pass


window=Interface()
window.show_all()
Gtk.main()
