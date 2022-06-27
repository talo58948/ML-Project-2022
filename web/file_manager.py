import librosa
import numpy as np
import librosa.display
from pydub import AudioSegment
import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

matplotlib.pyplot.switch_backend('Agg') 

UPLOADS_MP3 = 'web/temp/uploads_mp3'
SPECTROGRAMS = 'web/temp/spectrograms'
CLIPS = 'web/temp/clips'

# Takes uploaded file path and returns the path of the 3s long spectrogram generated for it.
def create_spec(file_path):
    name = os.path.basename(file_path)[:-4]
    clip_path = os.path.join(CLIPS, name+'.wav')
    spec_path = os.path.join(SPECTROGRAMS, name+'.png')
    try:
        clip_and_save(file_path, clip_path)
        create_spectrogram_of_clip(clip_path, spec_path)
    finally:
        os.remove(file_path) if os.path.exists(file_path) else "" #disposing of temporary files.
        os.remove(clip_path) if os.path.exists(clip_path) else ""
    return spec_path

def clip_and_save(file_path, clip_path, t1=47, t2=50):
    audio = AudioSegment.from_file(file_path)
    audio = audio[1000*t1:1000*t2]
    audio.export(clip_path, format='wav')

def create_spectrogram_of_clip(clip_path, spec_path):  
    y,sr = librosa.load(clip_path, duration=3)  
    mels = librosa.feature.melspectrogram(y=y,sr=sr)    
    fig = plt.Figure()  
    canvas = FigureCanvas(fig) 
    p = plt.imshow(librosa.power_to_db(mels,ref=np.max))   
    plt.savefig(spec_path)
    