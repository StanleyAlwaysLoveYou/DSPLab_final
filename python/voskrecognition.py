#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`

import argparse
import queue
import sys
import sounddevice
import pyaudio
import numpy as np
import json

from vosk import Model, KaldiRecognizer

command_dictionary = {
    'stop'     : 's',
    'left'     : 'l',
    'right'    : 'r',
    'backward' : 'b',
    'forward'  : 'f',
}

def get_text(data, samplerate = 16000, model=Model(lang="en-us")):
    

    ####### generate text ######
    rec = KaldiRecognizer(model, samplerate)
    rec.SetGrammar('["stop", "left", "right", "forward", "backward", "[unk]"]')
    rec.AcceptWaveform(data)
    output = json.loads(rec.Result())['text']
    print('voice detected: {}'.format(output))

    ###### classify the text ######
    for item in output.split(' ')[::-1]:
        key = command_dictionary.get(item, 0)
        if key:
            return key
    return 's'


def main():

    #######################################
    #      parameter definition           #
    #######################################

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 16000 # 44.1kHz sampling rate
    chunk = 8192 # 2^12 samples for buffer
    record_secs = 60 # seconds to record
    dev_index = 7 # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'test1.wav' # name of .wav file

    down_sample = 1 # down sampling 
    threshold = 309


    #######################################
    #      create pyaudio instantiation   #
    #######################################
    audio = pyaudio.PyAudio() 

    ###############################
    #     create pyaudio stream   #
    ###############################
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    wav = np.asarray([], dtype='int16')

    power_array = []
    previous_power = -20000

    ###############################################################################
    #      loop through stream and append audio chunks to frame array             #
    ###############################################################################

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
        will_be_process = (previous_power > threshold)
        previous_power = power
        
        ###############################
        #     voice recognition       #
        ###############################

        if(will_be_process):
            stream.stop_stream()
            
            ###### signal process ######
            
            command = get_text(previous_bytedata+data, samp_rate)
            print('command recognition: {}'.format(command))
        
            
            previous_power = -20000
            stream.start_stream()
            
        previous_bytedata = data


if __name__ == '__main__':
    main()
