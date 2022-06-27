import tensorflow.keras as keras
import enum

class Event(enum.Enum):
    train_start = 1
    train_end = 2
    epoch_start = 3
    epoch_end = 4
    batch_start = 5
    batch_end = 6
    test_start = 7
    test_end = 8
    test_batch_start = 9
    test_batch_end = 10

class Callback(keras.callbacks.Callback):
    def __init__(self, handler):
        self.handler = handler
    def on_train_begin(self, logs=None):
        self.handler(Event.train_start, logs)
    def on_train_end(self, logs=None):
        self.handler(Event.train_end, logs)
    def on_epoch_begin(self, epoch, logs=None):
        self.handler(Event.epoch_start, epoch, logs)
    def on_epoch_end(self, epoch, logs=None):
        self.handler(Event.epoch_end, epoch, logs)
    def on_train_batch_begin(self, batch, logs=None):
        self.handler(Event.batch_start, batch, logs)
    def on_train_batch_end(self, batch, logs=None):
        self.handler(Event.batch_end, batch, logs)
    def on_test_batch_begin(self, batch, logs=None):
        self.handler(Event.test_batch_start, batch, logs)
    def on_test_batch_end(self, batch, logs=None):
        self.handler(Event.test_batch_end, batch, logs)
    def on_test_begin(self, logs=None):
        self.handler(Event.test_batch_start, logs)
    def on_test_end(self, batch, logs=None):
        self.handler(Event.test_batch_start, batch, logs)