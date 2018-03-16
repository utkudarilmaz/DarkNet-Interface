#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  randimag.py
#  version : 0.2
#
#  Copyright 2012 Simon "Diceroll" Gaillard <gaillard.simon@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  dependencies : python3-gobject

import os
import random
import mimetypes
from gi.repository import Gtk, GdkPixbuf


class Main(object):
    def __init__(self):
        self.image_list = []

        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(600,800)
        window.set_title('random image viewer')
        window.set_border_width(16)
        window.connect_after('destroy', self.on_window_destroy)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)

        label = Gtk.Label("No Folder Selected : %s pictures" %
                          (len(self.image_list)))

        select_folder_button = Gtk.Button('Select Folder')
        select_folder_button.connect('clicked',
                                     self.on_select_folder_button_clicked,
                                     window, label)

        image = Gtk.Image()
        event_box = Gtk.EventBox()
        event_box.add(image)
        event_box.connect('button_press_event', self.on_image_clicked, image, label)

        vbox.pack_start(select_folder_button, False, False, 0)
        vbox.pack_start(event_box, True, True, 0)
        vbox.pack_end(label, False, False, 0)
        window.add(vbox)
        window.show_all()
        Gtk.main()

    def on_window_destroy(self, widget, data=None):
        Gtk.main_quit()

    def on_select_folder_button_clicked (self, widget, parent_window, label):
        '''Display a dialog to choose one or more folder'''
        dialog = Gtk.FileChooserDialog('Choose an image folder',
                                        parent_window,
                                        Gtk.FileChooserAction.SELECT_FOLDER,
                                        (Gtk.STOCK_CANCEL,
                                         Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN,
                                         Gtk.ResponseType.OK))
        dialog.set_select_multiple(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            folders = dialog.get_filenames()
            self.image_list = fetching_image_list(folders)
            label.set_text('selected %s folder(s) containing %s image(s)' %
                           (len(folders), len(self.image_list)))
        dialog.destroy()

    def on_image_clicked(self, widget, event, image, label):
        '''Display a random image from the selected folders'''
        image_size = (image.get_allocated_width(), image.get_allocated_height())
        if self.image_list:
            random_number = random.randint(0, len(self.image_list)-1)
            random_image = self.image_list[random_number]
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(random_image)
            image.set_from_pixbuf(scale_image(pixbuf, image_size))
            label.set_text(random_image)
        else:
            pass


def scale_image(pixbuf, size):
    ''' Scale larger image to fit in the window'''
    w = pixbuf.get_width()
    h = pixbuf.get_height()
    x, y = size

    # scale only if image is larger than the widget
    if w>x or h>y:
        L = min(x/w, y/h)
    else:
        L = 1

    new_pixbuf = pixbuf.scale_simple(w*L, h*L,
                                     GdkPixbuf.InterpType.BILINEAR)
    return new_pixbuf


def fetching_image_list(dir_path):
    ''' Retrieve a list of images'''
    mylist = []
    for directory in dir_path :
        for f in os.listdir(directory):
            file_type = mimetypes.guess_type(f)
            if 'image' in repr(file_type[0]):
                mylist.append(os.path.join(directory, f))
    return mylist


def main():
    app = Main()
    return 0

if __name__ == '__main__':
    main()
