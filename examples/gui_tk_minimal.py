#!/usr/bin/env python
"""
From tutorial:
http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/minimal-app.html
"""

import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.quit_button = None

    def create_widgets(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid()


app = Application()
app.master.title('Sample application')
app.mainloop()
