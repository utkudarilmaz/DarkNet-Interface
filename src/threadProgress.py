#!/usr/bin/python3

import threading
import os

class threadProgress(threading.Thread):

    def __init__(self,command,path):

        threading.Thread.__init__(self)

        self.command=command
        self.path=path

    def run(self):
        os.chdir(self.path)
        os.system(self.command)
        
