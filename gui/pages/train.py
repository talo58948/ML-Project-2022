from gui.pages.base import Page
import tkinter.ttk as ttk
import tkinter as tk
from model_api import train_model
from gui.callback import *

def get_stats_column(frame, stage):
    acc = ttk.Label(frame, text='')
    acc.pack(side='top', fill='both', expand=True)
    loss = ttk.Label(frame, text='')
    loss.pack(side='top', fill='both', expand=True)
    def update_stats(new_stats=None):
        if new_stats == None or new_stats == ():
            acc['text'] = ''
            loss['text'] = ''
        else:
            acc['text'] = f'{stage.upper()} ACCURACY: {str(round(new_stats[0], 3)*100)[:5]}%'
            loss['text'] = f'{stage.upper()} LOSS: {str(round(new_stats[1], 3))[:5]}'
    return update_stats

def get_progress_desc(prog_frame):
    precentage = ttk.Label(prog_frame, text='')
    precentage.pack(side='left', fill='both', expand=True)
    train_col = tk.Frame(prog_frame,)
    train_col.pack(side='left', fill='both', expand=True)
    vali_col = tk.Frame(prog_frame)
    vali_col.pack(side='left', fill='both', expand=True)
    
    train_stats_update = get_stats_column(train_col, 'train')
    vali_stats_update = get_stats_column(vali_col, 'validation')
    def update_precentage(new_prec=None):
        if new_prec == None:
            precentage['text'] = ''
        else:
            precentage['text'] = f'PROGRESS: {new_prec}%'
    def update_train_stats(new_stats=None):
        train_stats_update(new_stats)
    def update_vali_stats(new_stats=None):
        vali_stats_update(new_stats)
    return (update_precentage, update_train_stats, update_vali_stats)

class TrainPage(Page):
    def __init__(self, model_name, *args, **kwargs):
        Page.__init__(self, model_name, *args, **kwargs)
        start_button = ttk.Button(self, text='START', command=self.on_start)
        start_button.pack(side='top', fill='both', expand=True)
        
        progress_frame = tk.Frame(self)
        progress_frame.pack(side='top',fill='both', expand=True)

        self.pb = ttk.Progressbar(
            progress_frame, 
            orient='horizontal',
            mode='determinate',
        )
        self.pb.pack(side='top', fill='both', expand=True)
        self.update_precentage, self.update_train_stats, self.update_vali_stats = get_progress_desc(progress_frame)

    def on_start(self):
        Page.run_model(self.activate_scripts, args=(), use_model=False)
        
    def activate_scripts(self):
        def update_progressbar(num):
            self.pb['value'] = num
            if num == 0:
                self.update_precentage()
            else:
                self.update_precentage(f'{round(self.pb["value"])}')
        def handle_callback(event, *args):
            if event == Event.epoch_start:
                update_progressbar(0)
            
            elif event == Event.epoch_end:
                update_progressbar(100)
                new_stats = args[1]
                self.update_vali_stats((new_stats['val_accuracy'], new_stats['val_loss']))
            
            elif event == Event.batch_end:
                update_progressbar(100 * int(args[0]) / 99)
                new_stats = args[1]
                self.update_train_stats((new_stats['accuracy'], new_stats['loss']))
            
            elif event == Event.batch_start:
                if Page.model_thread_exit_event.is_set():
                    update_progressbar(0)
                    self.update_train_stats()
                    self.update_vali_stats()
                    Page.stop_model()

        train_and_save(handle_callback, model_ver=self.model_name.name)
        Page.stop_model()

def train_and_save(handler, model_ver='_gui'):
    callback = Callback(handler)
    train_model(model_ver=model_ver, callbacks=[callback])

