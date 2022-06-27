import numpy as np
from tensorflow.keras.utils import img_to_array, load_img
from tensorflow.keras.models import model_from_json

class_labels = ['blues 🎵', 'classical 🏛️', 'disco ✨', 'hiphop 🔥', 'metal 😈', 'pop 🎉', 'rock 🤘']
def predict(image_path, model):
    image_data = load_img(image_path, color_mode='rgba', target_size=(288,432))

    image = img_to_array(image_data)   
    image = np.reshape(image,(1,288,432,4))   
    prediction = model.predict(image/255)   
    prediction = prediction.reshape((7,))     
    class_label = np.argmax(prediction)
    
    return class_labels[class_label].upper(), prediction

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
    