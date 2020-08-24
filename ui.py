# import sys
# from PyQt5.QtWidgets import  QApplication, QWidget, QMainWindow, QPushButton, QAction
# from PyQt5.QtGui import  QIcon
# from PyQt5.QtCore import pyqtSlot

# class App(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.title = 'Feature-Flow-App'
#         self.left = 10
#         self.top = 10
#         self.width = 640
#         self.height = 480
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         mainMenu = self.menuBar()
#         fileMenu = mainMenu.addMenu('File')
#         helpMenu = mainMenu.addMenu('Help')

#         exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
#         exitButton.setShortcut('Ctrl+Q')
#         exitButton.setStatusTip('Exit Application')
#         exitButton.triggered.connect(self.close)
#         fileMenu.addAction(exitButton)

#         self.statusBar().showMessage('Message in statusbar')
#         self.show()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())

# import tkinter as tk

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()
#         self.create_widgets()

#     def create_widgets(self):
#         self.hi_there = tk.Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")

#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.pack(side="bottom")

#     def say_hi(self):
#         print("hi there, everyone!")

# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()

# import gi
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk

# def on_activate(app):
#     win = Gtk.ApplicationWindow(application=app)
#     btn = Gtk.Button(label="Hello, World!")
#     btn.connect('clicked', lambda x: win.destroy())
#     win.add(btn)
#     win.show_all()

# app = Gtk.Application(application_id='org.gtk.Example')
# app.connect('activate', on_activate)
# app.run(None)

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")


builder = Gtk.Builder()
builder.add_from_file("example.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()