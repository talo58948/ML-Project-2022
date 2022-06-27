import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import threading
import sys

class Page(tk.Frame):
    model_thread : threading.Thread = None
    model_thread_exit_event = threading.Event()
    model_name = None
    def __init__(self, model_name, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        if Page.model_name == None:
            Page.model_name = model_name

        stop_button_frame = tk.Frame(self)
        stop_button_frame.pack(side='bottom', expand=True, fill='both')

        self.stop_model_button = ttk.Button(stop_button_frame, text='STOP MODEL', command=self.on_press_stop)
        self.stop_model_button.pack(side='left', fill='both', expand=True)

    def on_press_stop(self):
        if not Page.model_running:
            return
        if messagebox.askyesno(title='Confirmation', message='Are You Sure You Want to Terminate this Model Session'):
            Page.model_thread_exit_event.set()
        

    def show(self):
        self.lift()

    def before_change_model():
        if Page.model_name.model_exists_on_path():
            messagebox.showwarning(title='Warning', message='A Model With That Name Already Exists,\nDefaulting to Name "gui"')
            Page.model_name.name = 'gui'

    def before_use_model():
        if not Page.model_name.model_exists_on_path():
            messagebox.showwarning(title='Warning', message='A Model With That Name Doesn\'t Exist,\nDefaulting to Version "10.4"')
            Page.model_name.name = '10.4'

    model_running = False
    def run_model(func, args, use_model=True):
        if Page.model_running:
            messagebox.showerror(title='Error', message='An Instance of the Model is Already Running,\nTerminate It First Before Continuing')
            return
        change_model = not use_model
        if use_model:
            Page.before_use_model()
        if change_model:
            Page.before_change_model()

        Page.model_thread = threading.Thread(target=Page.wrapper_func, args=(func, args))
        Page.model_thread.daemon = True
        Page.model_thread.start()
        Page.model_running = True

    def wrapper_func(target, args=()):
        try:
            target(*args)
        except Exception as e:
            messagebox.showerror(title='Exception', message=e)
        finally:
            Page.stop_model()
    # MUST be called from model thread
    def stop_model():
        Page.model_running = False
        Page.model_thread_exit_event.clear()
        sys.exit()

class ModelName:
    def __init__(self):
        self.name = ''
    def change(self, new):
        self.name = new
    def get_model_and_weights_paths(self):
        model_path = os.path.join(f'saves/model/model{self.name}.json')
        weights_path = os.path.join(f'saves/weights/model_weights{self.name}.h5')
        return model_path, weights_path
    def model_exists_on_path(self):
        model_path, weights_path = self.get_model_and_weights_paths()
        return os.path.isfile(model_path) and os.path.isfile(weights_path)