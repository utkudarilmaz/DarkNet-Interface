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

    def __init__(self,imageoutput,spinner,command,path,textBuffer):

        threading.Thread.__init__(self)
        self.imageoutput=imageoutput
        self.spinner=spinner
        self.command=command
        self.path=path
        self.outputpath=self.path+"/predictions.png"
        self.textBuffer=textBuffer

    def run(self):

        args=shlex.split(self.command)

        tmpWrite = open("tmpout", "wb")
        self.tmpRead = open("tmpout","r")

        t=TextBufferSetter(self.textBuffer,self.tmpRead)

        process=Popen(args, cwd=self.path, stdout = tmpWrite, stderr = tmpWrite, bufsize = 1)
        t.start()
        process.wait()

        tmpWrite.close()
        self.tmpRead.close()

        self.spinner.stop()
        self.tmpRead.close()
        pix=GdkPixbuf.Pixbuf.new_from_file_at_scale(self.outputpath,550,700,True)
        self.imageoutput.set_from_pixbuf(pix)

class TextBufferSetter(threading.Thread):

    def __init__(self,textBuffer,tmpRead) :

        threading.Thread.__init__(self)
        self.textBuffer = textBuffer
        self.tmpRead=tmpRead

    def run(self) :

        while not self.tmpRead.closed :
            self.textBuffer.set_text(self.tmpRead.read())
