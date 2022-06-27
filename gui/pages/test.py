from gui.pages.base import Page
from tkinter import ttk
import tkinter as tk
from model_api import test_model
from gui.callback import *

class TestPage(Page):
    def __init__(self, model_name, *args, **kwargs):
        Page.__init__(self, model_name, *args, **kwargs)
        
        start_button = ttk.Button(self, text='RUN', command=self.on_start)
        start_button.pack(side='top', fill='both', expand=True)

        vali_frame = tk.Frame(self)
        vali_frame.pack(side='top', fill='both', expand=True)

        self.vali_acc = ttk.Label(vali_frame, text='')
        self.vali_loss = ttk.Label(vali_frame, text='')
        self.vali_desc = ttk.Label(vali_frame, text='Run Evaluation To Get Test Results')

        self.vali_desc.pack(side='left', fill='both', expand=True)
        self.vali_acc.pack(side='left', fill='both', expand=True)
        self.vali_loss.pack(side='left', fill='both', expand=True)

        
    def on_start(self):
        Page.run_model(self.activate_scripts, args=(), use_model=True)
    def activate_scripts(self):
        def handle_callback(event, *args):
            if event == Event.test_batch_end:
                if Page.model_thread_exit_event.is_set():
                    Page.stop_model()
        loss, acc = run_test_model(handle_callback, self.model_name.name)
        
        acc = str(100 * acc)[:5]
        loss = str(loss)[:5]
        self.vali_desc['text'] = ''
        self.vali_acc['text'] = f'Validation Accuracy: {acc}%'
        self.vali_loss['text'] = f'Validation Loss: {loss}'
        Page.stop_model()


def run_test_model(handler, model_ver='10.4'):
    callback = Callback(handler)
    return test_model(model_ver, [callback])