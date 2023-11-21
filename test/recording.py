import pyaudio
from scipy.io import wavfile
import numpy as np
import time
import sounddevice
import matplotlib.pyplot as plt



form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 16000 # 44.1kHz sampling rate
chunk = 8192 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 7 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file
down_sample = 1 # down sampling 

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("recording")
wav = np.asarray([], dtype='int16')

power_array = []
previous_power = -20000

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    
    ###############################
    #     record the rawdata      #
    ###############################
    rawdata = np.asarray([ 256 * data[i+1] + data[i] for i in range(0, len(data), 2)], dtype='uint16')
    rawdata = np.asarray(rawdata[::down_sample], dtype='int16')
    
    ###############################
    #     check the power         #
    ###############################
    power = np.average(np.abs(rawdata))
    print('average abs value of this chunk: {}'.format(power))
    power_array.append(np.average(np.abs(rawdata)))
    previous_power = power

        
        
    previous_data = rawdata
    previous_bytedata = data
    wav = np.concatenate((wav, rawdata))

##############################
#      print time domain     #
##############################
plt.figure('time domain')
x = [i/(samp_rate/down_sample) for i in range(len(wav))]
plt.plot(x, wav)
plt.xlabel('time [s]')
plt.savefig('figure/time_fs{}_down{}.png'.format(samp_rate, down_sample))
plt.vlines(x=[ chunk/samp_rate*i for i in range(0,int((samp_rate/chunk)*record_secs))], ymin=-10000, ymax=10000, color='r')
# plt.plot([ (chunk/samp_rate*i + chunk/samp_rate*(i+1))/2 for i in range(0,int((samp_rate/chunk)*record_secs))], power_array, marker='x', color='black', linestyle='None')

plt.show()


# save the audio frames as .wav file
print(np.asarray(wav, dtype='int16'))
wavfile.write(wav_output_filename, samp_rate, np.asarray(wav, dtype='int16'))
