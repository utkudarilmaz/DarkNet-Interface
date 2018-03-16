#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Separator(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(400, 200)
        self.connect("destroy", Gtk.main_quit)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box.set_homogeneous(True)
        self.add(box)

        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(separator, True, True, 0)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator, True, True, 0)

window = Separator()
window.show_all()

Gtk.main()
