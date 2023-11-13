import sounddevice
from scipy.io.wavfile import write

fs = 16000  # Sample rate
seconds = 1  # Duration of recording
for i in range(20):
    print('start {} times'.format(i))
    myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels = 1)
    sounddevice.wait()  # Wait until recording is finished
    write(f'stanleylin/right/testing{i:d}.wav', fs, myrecording)
