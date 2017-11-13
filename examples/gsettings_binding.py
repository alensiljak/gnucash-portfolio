#!/usr/bin/python3
"""
Source
https://marianochavero.wordpress.com/2012/04/03/short-example-of-gsettings-bindings-in-python/
"""
from gi.repository import Gtk, Gio
 
class Example(Gtk.Window):
 
    def __init__(self):
        # Setup the window with title and border width.
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL,
                                  title="Gsettings Switch Example",
                                  resizable=False,
                                  border_width=10)
        # Create and bind the Gtk Switch with the gsettings schema and its key.
        switch = Gtk.Switch()
        setting = Gio.Settings.new("org.gnome.desktop.background")
        setting.bind("show-desktop-icons", switch, "active", Gio.SettingsBindFlags.DEFAULT)
 
        # Create the label for the switch
        label = Gtk.Label("Show Icons on the Desktop")
 
        # Position the Switch and its Label inside a Horizontal child box.
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 40)
        box.pack_start(label, False, False, 10)
        box.pack_end(switch, False, False, 10)
 
        # Add the child box to the window
        self.add(box)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
 
if __name__ == "__main__":
    Example()