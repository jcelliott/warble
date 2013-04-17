#!/usr/bin/env python
# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np
import sys
from pylab import *

CHUNK = 4096

def read_pitch(wav):
    # open up a wave
    wf = wave.open(wav, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(CHUNK)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = RATE,
                    output = True)

    # read some data
    data = wf.readframes(CHUNK)
    pitches = {}
    time = 0
    # play stream and find the frequency of each chunk
    while len(data) == CHUNK*swidth:
        # write data out to the audio stream
        stream.write(data)
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                             data))*window
        # Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        freq = 0
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            freq = (which+x1)*RATE/CHUNK
            # print "The freq is %f Hz." % (freq)
            pitches[time] = freq
        else:
            freq = which*RATE/CHUNK
            # print "The freq is %f Hz." % (freq)
            pitches[time] = freq
        # read some more data
        data = wf.readframes(CHUNK)
        time += 1

    if data:
        stream.write(data)
    stream.close()
    p.terminate()

    return pitches

if __name__ == "__main__":
    pitch = read_pitch(sys.argv[1])

    # filter out values that are too high
    for k, v in pitch.items():
        if v > 600:
            del pitch[k]

    # print pitch
    plot(pitch.keys(), pitch.values())
    show()

