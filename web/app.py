import os
from flask import Flask, request, render_template
from waitress import serve
from web.predictor import load_model, predict
from web.file_manager import create_spec

model = None

def init_model(model_path, weights_path):
    global model
    model = load_model(model_path, weights_path)

def get_genre(file_path):
    spec_path = create_spec(file_path)
    try:
        genre, prediction = predict(spec_path, model)
    finally:
        os.remove(spec_path) if os.path.exists(spec_path) else ""
    return genre, prediction

# create folder for uploaded data
FOLDER = 'web/uploaded'
os.makedirs(FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        field, data = next(request.files.items())
        print('field:', field)
        print('filename:', data.filename)
        
        if data.filename:
            file_path = os.path.join(FOLDER, data.filename)
            data.save(file_path)
            try:
                genre = get_genre(file_path)[0]
                return render_template('index.html',genre=genre)
            except Exception as e:
                print('exception occured!')
                print(e)
                return render_template('index.html', exception=e)
        return render_template('index.html', exception='unknown')
            

def host_webapp():
    serve(app, host='0.0.0.0', port=8000)
if __name__ == '__main__':
    host_webapp()