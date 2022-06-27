from genre_model import genre_model
from data_gen import create_generators
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt

VERSION = 10.4
MODEL_SAVE_PATH = f'saves/model/model{VERSION}.json'
WEIGHTS_SAVE_PATH = f'saves/weights/model_weights{VERSION}.h5'
HISTORY_SAVE_PATHS = f'saves/history/acc{VERSION}.png', f'saves/history/loss{VERSION}.png'
MODEL_IMAGE_SAVE_PATH = f'saves/images/model{VERSION}.png'

def init_vars(model_version=None):
    if model_version == None:
        model_version = VERSION
    global MODEL_IMAGE_SAVE_PATH, MODEL_SAVE_PATH, HISTORY_SAVE_PATHS, WEIGHTS_SAVE_PATH
    MODEL_SAVE_PATH = f'saves/model/model{model_version}.json'
    WEIGHTS_SAVE_PATH = f'saves/weights/model_weights{model_version}.h5'
    HISTORY_SAVE_PATHS = f'saves/history/acc{model_version}.png', f'saves/history/loss{model_version}.png'
    MODEL_IMAGE_SAVE_PATH = f'saves/images/model{model_version}.png'

def fit_model(model, data_gens, epochs=70, callbacks=[]):
    train_gen, vali_gen = data_gens

    checkpoint = ModelCheckpoint(WEIGHTS_SAVE_PATH, monitor='val_accuracy',
                                save_weights_only=True, mode='max', verbose=1, save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_accuracy', mode='max', patience=8)
    callbacks = callbacks + [checkpoint, early_stopping]
    history = model.fit(
        x=train_gen,
        epochs=epochs,
        validation_data=vali_gen,
        callbacks=callbacks
    )
    return history
    
def save_history(history, acc_path, loss_path):
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(acc_path)
    # summarize history for loss
    plt.clf()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(loss_path)


def json_save_model(model, save_weights=True):
    model_json = model.to_json()
    if save_weights:
        model.save_weights(WEIGHTS_SAVE_PATH)
    with open(MODEL_SAVE_PATH, 'w') as json_file:
        json_file.write(model_json)

def main(model=None):
    if model == None:
        model = genre_model()
    # model = genre_model() # our Genre Recognition model
    plot_model(model, to_file=MODEL_IMAGE_SAVE_PATH, show_shapes=True, show_layer_names=True)
    data_gens = create_generators(batch_size=64)
    hist = fit_model(model, data_gens, epochs=100)
    json_save_model(model, False)
    save_history(hist, acc_path=HISTORY_SAVE_PATHS[0], loss_path=HISTORY_SAVE_PATHS[1])


if __name__ == '__main__':
    main(model=genre_model())