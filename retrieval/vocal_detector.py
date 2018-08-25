import os
import sys
import keras
from keras.models import load_model 
import numpy as np
import librosa
 
SCHLUTER_CNN_PATH = 'static/models/cnn_20180601-1.h5'
THRESHOLD = 0.5 
INPUT_SIZE = 115 

def load_svd_model(model_path): 
    model = load_model(model_path)
    return model 

def log_melgram(y, sr=22050, n_fft=1024, hop_length=315, n_mels=80, fmin=0.0, fmax=8000):
    melspec = librosa.feature.melspectrogram(y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels, fmin=fmin, fmax=fmax, power=1.0)
    log_melspec = librosa.amplitude_to_db(melspec)
    return log_melspec

def infer(audio_filepath):
    # Load and preprocess song 
    # Input size to the model should be (80, 115)
    y, _ = librosa.load(audio_filepath, sr=22050)
    melgram = log_melgram(y)

    # load trained model 
    model = load_svd_model(SCHLUTER_CNN_PATH)
    print(model.summary())

    # predict 
    predictions = [] 
    for i in range(melgram.shape[1]): 
        if i + INPUT_SIZE > melgram.shape[1]:
            break
        segment = melgram[:, i:i+INPUT_SIZE]
        segment = np.expand_dims(segment, 2)
        segment = np.expand_dims(segment, 0)
        pred = model.predict(segment)

        pred[pred >= THRESHOLD] = True
        pred[pred < THRESHOLD] = False
        pred = pred.astype(int)
        predictions.append(pred[0][0])

    yes_vocal = np.count_nonzero(predictions)
    print ("vocal percentage %.2f"%(yes_vocal/len(predictions)))


if __name__ == '__main__':
    test_audio = '../28f3c0fd0fa702cbe1cf941bd82d751bb2db9db8.wav'
    # test_audio = '../4c9524aa1963c47e2512dea80597bba9ad25fb50.wav' # shofukan
    # test_audio = '../99c122521a69978ad3e4f2ddc23a311d9d922da6.wav' # ryuichi
    infer(test_audio)
