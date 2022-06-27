from gui.pages.base import Page
from tkinter import ttk
import tkinter as tk
import os
from web.app import host_webapp, init_model

class HostPage(Page):
    def __init__(self, model_name, *args, **kwargs):
        Page.__init__(self, model_name, *args, **kwargs)
        host_button = ttk.Button(self, text='HOST', command=self.start_hosting)
        host_button.pack(side='top', fill='both', expand=True)

        self.text = ttk.Label(self, text='')
        self.text.pack(side='top', fill='both', expand=True)

    def start_hosting(self):
        Page.run_model(func=self.activate_scripts, args=(), use_model=True)
        self.text['text'] = 'Open Browser on localhost:8000'

    def activate_scripts(self):
        model_path, weights_path = self.model_name.get_model_and_weights_paths()
        init_model(model_path, weights_path)
        host_webapp()
