from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from data_gen import create_generators
from training_testing import fit_model, init_vars, json_save_model
from genre_model import genre_model

def load_model(model_path, weights_path):
    # load json and create model
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(weights_path)
    print("Loaded model from disk")
    return loaded_model

def test_model(model_ver, callbacks):
    model_save_path = f'saves/model/model{model_ver}.json'
    weights_save_path = f'saves/weights/model_weights{model_ver}.h5'
    model = load_model(model_save_path, weights_save_path)

    opt = Adam(learning_rate=5e-5)
    model.compile(optimizer=opt, loss='categorical_crossentropy',metrics=['accuracy'])

    vali_data = create_generators()[1] # taking vali generator
    loss, acc = model.evaluate(vali_data, callbacks=callbacks, verbose=0)
    return (loss, acc)

def train_model(model_ver, callbacks):
    model = genre_model()
    data_gens = create_generators()
    init_vars(model_ver)
    fit_model(model, data_gens=data_gens,epochs=20, callbacks=[callbacks])
    json_save_model(model, save_weights=False) # already saving best weights in checkpoint callback
