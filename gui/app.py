import tkinter as tk
from tkinter import ttk
from gui.pages.base import ModelName
from gui.pages.test import TestPage
from gui.pages.train import TrainPage
from gui.pages.host import HostPage
import sv_ttk

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.model_name = ModelName()
        sv_ttk.set_theme('dark')

        p1 = TrainPage(self.model_name ,self)
        p2 = TestPage(self.model_name, self)
        p3 = HostPage(self.model_name, self)

        nav_buttonframe = tk.Frame(self)
        modelname_frame = tk.Frame(self)
        container = tk.Frame(self)

        nav_buttonframe.pack(side="top", fill="x", expand=False)
        modelname_frame.pack(side='top', fill='x', expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        model_input_label = ttk.Label(modelname_frame, text='Model Name:', justify='center')
        model_name_input = ttk.Entry(modelname_frame)
        submit_button = ttk.Button(modelname_frame, text="Submit", command=lambda: self.update_model_name(model_name_input.get()))
        b1 = ttk.Button(nav_buttonframe, text="Training", command=p1.show)
        b2 = ttk.Button(nav_buttonframe, text="Testing", command=p2.show)
        b3 = ttk.Button(nav_buttonframe, text="Hosting Web App", command=p3.show)
        
        model_input_label.pack(side='left', expand=True, fill='both')
        model_name_input.pack(side='left', expand=True, fill='both')
        submit_button.pack(side='left', expand=True, fill='both')
        b1.pack(side="left", expand=True, fill='both')
        b2.pack(side="left", expand=True, fill='both')
        b3.pack(side="left", expand=True, fill='both')
        

        p1.show()

    def update_model_name(self, new_name):
        self.model_name.change(new_name)
def run():
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("600x400")
    root.resizable(False, False)
    root.title('My GUI App')
    root.iconbitmap('gui/music.ico')
    root.mainloop()

if __name__ == "__main__":
    run()