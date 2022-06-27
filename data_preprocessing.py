from multiprocessing import Pool, Value
import numpy as np
import os
import matplotlib.pyplot as plt
import librosa
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import shutil
import random
from pydub import AudioSegment

GENRES = 'blues classical disco pop hiphop metal rock'.split()
DATA_RELATIVE_PATH = 'gtzan_dataset\genres_original'
FIXED_DATA_RELATIVE_PATH = 'content'

# prepares the folders structure
def prepare_data_folders():
    os.makedirs(os.getcwd() + '/content/spectrograms/train', exist_ok=True)
    os.makedirs(os.getcwd() + '/content/spectrograms/test', exist_ok=True)
    
    for g in GENRES:
        path_audio = os.path.join(os.getcwd() + '/content/clips', g)
        path_train = os.path.join(os.getcwd() + '/content/spectrograms/train', g)
        path_test = os.path.join(os.getcwd() + '/content/spectrograms/test', g)
        os.makedirs(path_audio, exist_ok=True)
        os.makedirs(path_train, exist_ok=True)
        os.makedirs(path_test, exist_ok=True)

# cuts all the audio files present in the dataset to 3sec clips each and saves it to clips folder. 
def cut_all_and_save():
    global clip_count
    for g in GENRES:
        song_index = 0
        genre_path = os.path.join(DATA_RELATIVE_PATH, g)

        for song_file in os.listdir(genre_path):
            if song_file.endswith('.wav'):
                sp = os.path.join(genre_path, song_file)
                cof = os.path.join(FIXED_DATA_RELATIVE_PATH, 'clips', g)
                cut_song_to_clips(song_path=sp, clips_output_folder=cof, genre_name=g, song_index=song_index)
                song_index += 1
                
    
# takes songs path, clips output folder, genre name and song index and generates clips, saving them to the output folder.
def cut_song_to_clips(song_path, clips_output_folder, genre_name, song_index):
    for c in range(0,10):
        t1 = 3*(c)*1000
        t2 = 3*(c+1)*1000
        clipAudio = AudioSegment.from_wav(song_path)
        clip = clipAudio[t1:t2]
        clip_path = os.path.join(clips_output_folder, f'{genre_name}_song_{song_index}_clip_{c}.wav')
        clip.export(clip_path, format='wav')

# goes through all the clips in clips and converts them into spectrograms, saving it to spectrograms directory, while preserving folder structure.
def generate_spectrograms(proc_num=4):
    counter = Value('I', 0)
    with Pool(proc_num, initializer=_process_init, initargs=(counter,)) as pool:
        pool.starmap(_generate_save_spec, _args_gen())
        
def _process_init(c): #initializing global value, counter to a newly made process
    global counter
    counter = c

def _args_gen():
    current_clip_index = 0
    for g in GENRES:
        genre_path = os.path.join(FIXED_DATA_RELATIVE_PATH, 'clips', g)
        for filename in os.listdir(genre_path):
            if filename.endswith('.wav'):
                clip_path = os.path.join(genre_path, filename)
                spec_save_path = os.path.join(FIXED_DATA_RELATIVE_PATH, 'spectrograms', 'train', g, filename[:-4] + '.png')
                yield [clip_path, spec_save_path]
                current_clip_index += 1

# generates and saves a spectrogram of a specific clip. takes the clip's path and the desired path for the spectrogram to be saved in.
def _generate_save_spec(clip_path, spec_path):
    if not os.path.exists(spec_path):
        y,sr = librosa.load(clip_path, duration=3)
        mel_s = librosa.feature.melspectrogram(y=y,sr=sr)
        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        p = plt.imshow(librosa.power_to_db(mel_s, ref=np.max))
        plt.savefig(spec_path)
        
    with counter.get_lock():
        counter.value += 1
        print(f'made {counter.value}/7000')

# moves a portion of the spectrograms to the test directory.
def move_to_test():
    train_dir = 'content/spectrograms/train'
    test_dir = 'content/spectrograms/test'
    for g in GENRES:
        filenames = os.listdir(os.path.join(train_dir, g))
        random.shuffle(filenames)
        test_files = filenames[:100]
        for f in test_files:
            from_path = os.path.join(train_dir, g, f)
            to_path = os.path.join(test_dir, g, f)
            shutil.move(from_path, to_path)

def main():
    prepare_data_folders()
    cut_all_and_save()
    generate_spectrograms()
    move_to_test()
    
if __name__ == '__main__':
    main()
