#!/usr/bin/python3

import threading
import os
import gi

gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository import GObject

class ThreadProgress(threading.Thread):

    def __init__(self,imageoutput,spinner,command,path):

        threading.Thread.__init__(self)
        self.imageoutput=imageoutput
        self.spinner=spinner
        self.command=command
        self.path=path
        self.outputpath=self.path+"/predictions.png"


    def run(self):
        os.chdir(self.path)
        os.system(self.command)
        self.spinner.stop()
        pix=GdkPixbuf.Pixbuf.new_from_file_at_size(self.outputpath,550,700)
        self.imageoutput.set_from_pixbuf(pix)
