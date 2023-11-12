from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import numpy as np
import sounddevice
from hmmlearn import hmm
import os
import glob
from trainer import HMMTrainer
import pickle
path1 = "backward/"
path2 = "forward/"
path3 = "left/"
path4 = "right/"
path5 = "stop/"
command = ['backward', 'forward', 'left', 'right', 'stop']
pathes = [path1, path2, path3, path4, path5]


for i in range(0, len(command)): 
    with open(f"thebest/hmm{i:d}.pkl", "rb") as file: 
        hmm_trainer = pickle.load(file)
        hmm_models.append((hmm_trainer, i))
        
        
precision = []
for i in range(0, len(pathes)):
    correct = 0
    total = 0
    for filename in glob.glob(os.path.join(pathes[i], '*.wav')):
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
        if index == i: 
            correct += 1
        total += 1
    precision.append(correct/total)
print(precision)
