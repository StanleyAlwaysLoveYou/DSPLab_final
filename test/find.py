import pyaudio
import wave

p = pyaudio.PyAudio()
print(pyaudio.PyAudio().get_device_count())
for ii in range(p.get_device_count()):
    dev = p.get_device_info_by_index(ii)
    print((ii,dev['name'],dev['maxInputChannels']))