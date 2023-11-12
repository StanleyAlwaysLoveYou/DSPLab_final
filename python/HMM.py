from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
import sounddevice
from hmmlearn import hmm
import os
import glob
from trainer import HMMTrainer
import pickle

command = ['backward', 'forward', 'left', 'right', 'stop']

fs = 16000  # Sample rate
seconds = 1  # Duration of recording
hmm_models = []

for i in range(0, len(command)): 
    with open(f"thebest/hmm{i:d}.pkl", "rb") as file: 
        hmm_trainer = pickle.load(file)
        hmm_models.append((hmm_trainer, i))
samplerate, data = wav.read(filename)
data_int16 = np.asarray(data / np.abs(data).max() * (1 << 15), np.int16)
mfcc_feat = mfcc(data_int16, samplerate, numcep=20)
scores = []
for item in hmm_models:
    hmm_model, label = item
    score = hmm_model.get_score(mfcc_feat)
    scores.append(score)
index=np.array(scores).argmax()
print(command[index])
       





