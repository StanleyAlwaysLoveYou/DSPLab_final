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
path1 = "dataset/backward/"
path2 = "dataset/forward/"
path3 = "dataset/left/"
path4 = "dataset/right/"
path5 = "dataset/stop/"
command = ['backward', 'forward', 'left', 'right', 'stop']
pathes = [path1, path2, path3, path4, path5]

fs = 16000  # Sample rate
seconds = 1  # Duration of recording
hmm_models = []

# for i in range(30):
#     print('start {} times'.format(i))
#     myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels = 1)
#     sounddevice.wait()   
#     write(f'testing{i:d}.wav', fs, myrecording)

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

# for i in range(30):
#     rate, sig = wav.read(f'./testing{i:d}.wav')
#     sig = np.asarray(sig / np.abs(sig).max() * (1 << 15), np.int16)
#     mfcc_feat = mfcc(sig, rate, numcep=20)
#     scores = []
#     for item in hmm_models:
#         hmm_model, label = item
#         score = hmm_model.get_score(mfcc_feat)
#         scores.append(score)
#     index=np.array(scores).argmax()
#     print(command[index], scores)

# hmm_models = []   
# for i in range(len(command)): 
#     with open(f"hmm_noaverage_n=25/hmm{i:d}.pkl", "rb") as file: 
#         hmm_trainer = pickle.load(file)
#         hmm_models.append((hmm_trainer, i))


# for i in range(10):
#     rate, sig = wav.read(f'./testing{i:d}.wav')
#     sig = np.asarray(sig / np.abs(sig).max() * (1 << 15), np.int16)
#     mfcc_feat = mfcc(sig, rate, numcep = 16)
#     scores = []
#     for item in hmm_models:
#         hmm_model, label = item
#         score = hmm_model.get_score(mfcc_feat)
#         scores.append(score)
#     index=np.array(scores).argmax()
#     print(command[index])
# print("here")

# hmm_models = []   
# for i in range(len(command)): 
#     with open(f"hmm_no_average_n=20_16/hmm{i:d}.pkl", "rb") as file: 
#         hmm_trainer = pickle.load(file)
#         hmm_models.append((hmm_trainer, i))


# for i in range(10):
#     rate, sig = wav.read(f'./testing{i:d}.wav')
#     sig = np.asarray(sig / np.abs(sig).max() * (1 << 15), np.int16)
#     mfcc_feat = mfcc(sig, rate, numcep = 16)
#     scores = []
#     for item in hmm_models:
#         hmm_model, label = item
#         score = hmm_model.get_score(mfcc_feat)
#         scores.append(score)
#     index=np.array(scores).argmax()
#     print(command[index])
