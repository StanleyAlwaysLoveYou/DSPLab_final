import pyaudio
from scipy.io import wavfile
import numpy as np
import time
import sounddevice
import matplotlib.pyplot as plt
import motor_control


teensy_port = '/dev/ttyACM1'  # Teensy Serial port
bt_port = '/dev/rfcomm0'    # HC-05 port
bt_baud = 38400

commands = ['f', 'b', 's', 'l', 'r']




form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 8000 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 20 # seconds to record
dev_index = 7 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file
down_sample = 4 # down sampling 

threshold = 300

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
    
    # record the rawdata
    rawdata = np.asarray([ 256 * data[i+1] + data[i] for i in range(0, len(data), 2)], dtype='uint16')
    rawdata = np.asarray(rawdata[::down_sample], dtype='int16')
    
    # check the power
    power = np.average(np.abs(rawdata))
    print('average abs value of this chunk: {}'.format(power))
    power_array.append(np.average(np.abs(rawdata)))
    will_be_process = (previous_power > threshold)
    previous_power = power
    
    # voice recognition
    if(will_be_process):
        stream.stop_stream()
        window = np.concatenate((previous_data, rawdata))
        
        ##### signal process ##### TODO
        
        
        # send command
        motor_control.send('l')
        
        previous_power = -20000
        stream.start_stream()
        
        
    previous_data = rawdata
    

    
        
    # play rawdata
    # sounddevice.play(rawdata, samplerate=samp_rate/down_sample, blocking=False)
    
    # concatenate the rawdata to whole waveform
    wav = np.concatenate((wav, rawdata))


print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()


# print time domain
plt.figure('time domain')
x = [i/(samp_rate/down_sample) for i in range(len(wav))]
plt.plot(x, wav)
plt.xlabel('time [s]')
plt.savefig('figure/time_fs{}_down{}.png'.format(samp_rate, down_sample))
plt.vlines(x=[ chunk/samp_rate*i for i in range(0,int((samp_rate/chunk)*record_secs))], ymin=-10000, ymax=10000, color='r')
plt.plot([ (chunk/samp_rate*i + chunk/samp_rate*(i+1))/2 for i in range(0,int((samp_rate/chunk)*record_secs))], power_array, marker='x', color='black', linestyle='None')

plt.show()

'''
# save the audio frames as .wav file
print(np.asarray(wav, dtype='int16'))
wavfile.write(wav_output_filename, samp_rate, np.asarray(wav, dtype='int16'))
'''
