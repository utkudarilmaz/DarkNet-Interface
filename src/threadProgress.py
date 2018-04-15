#!/usr/bin/python3

import threading
import os
import gi
import shlex
from subprocess import Popen, PIPE

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
        args=shlex.split(self.command)
        process=Popen(args, cwd=self.path)
        process.wait()
        self.spinner.stop()
        pix=GdkPixbuf.Pixbuf.new_from_file_at_scale(self.outputpath,550,700,True)
        self.imageoutput.set_from_pixbuf(pix)
