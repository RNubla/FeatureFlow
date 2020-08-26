from tkinter import *
import tkinter.filedialog as fdialog
from tkinter.ttk import Progressbar
import os
from pathlib import Path
from split_video_sections import HighResVideos

class Application:
    def __init__(self):
        self.windowTitle = ' Feature Flow App '
        self.windowSize = '640x360'

        self.root = Tk(className=self.windowTitle)
        self.root.geometry(self.windowSize)

        # File menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open', command=self.open_video)
        self.file_menu.add_command(label='Exit', command=self.root.quit)
        self.help_menu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='About')

        browseBtn = Button(self.root, text='Input Video', command=self.open_video)
        self.input_path_label = Label(self.root)

        browseBtn.grid(row=0)
        self.input_path_label.grid(row=0, column=1)

        self.interp_number = Entry(self.root, textvariable=2)
        self.interp_number.grid(row=0, column=2)

        start_btn = Button(self.root, text='Start Interpolation', command=self.start_interp)
        start_btn.grid(row=0, column=3)

        outputBtn = Button(self.root, text='Output', command=self.choose_output)
        self.output_path_label = Label(self.root)

        outputBtn.grid(row=1, column=0)
        self.output_path_label.grid(row=1, column=1)
        

        progress_bar = Progressbar(self.root, orient= HORIZONTAL, length = 100, mode = 'determinate')

    # def bar(self):
        
    def choose_output(self):
        cwd = os.getcwd()
        output_dir = Path(cwd + '/output')
        self.save_folder = fdialog.askdirectory(initialdir = output_dir)
        self.output_path_label.config(text=self.save_folder)
        print(self.save_folder)

    def open_video(self):
        cwd = os.getcwd()
        input_dir = Path(cwd + '/input')
        self.video_file = fdialog.askopenfilename(initialdir = input_dir, filetypes = (('Video Files', '.mp4'), ('All Files', '*.*')), title = 'Choose a file')
        self.input_path_label.config(text=self.video_file)
        print(self.video_file)
    
    def start_interp(self):
        interp = HighResVideos((self.video_file), self.interp_number.get())
        interp.create_dir()
        interp.remove_dup_frames()
        interp.run_splitter()
        interp.run_feature_flow()
        interp.stitch_sections()
        interp.delete_files()


if __name__ == "__main__":
    app = Application()
    app.root.mainloop()