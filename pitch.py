#!/usr/bin/env python
# Read in a wav file, find the pitches, and plot them

import sys
import os.path
from pylab import *
from aubio import source, pitch

class Pitch:
    def __init__(self, pitch, time):
        self.pitch = pitch
        self.time = time

    def __str__(self):
        return "%f:   %f" % (self.time, self.pitch)
    def __repr__(self):
        return "%f:   %f\n" % (self.time, self.pitch)
    def __eq__(self, other):
        return self.time == other.time and self.pitch == other.pitch

def read_pitch(filename, chunk):

    win_s = chunk # fft size
    hop_s = win_s # hop size

    samplerate = 0
    # if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    pitch_o = pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("freq")

    pitches = []
    # times = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        cur_pitch = pitch_o(samples)[0]
        # print "%f %f" % (total_frames / float(samplerate), pitch)
        pitches.append(Pitch(cur_pitch, total_frames / float(samplerate)))
        total_frames += read
        if read < hop_s: break

    # print pitches
    return pitches

def filter_pitch(pitches, limit):
    # filter out values that are too high
    filter_pitch = []

    for i in range(len(pitches)):
        if pitches[i].pitch > limit or pitches[i].pitch == 0:
            filter_pitch.append(pitches[i])

    pitches = [p for p in pitches if p not in filter_pitch]

    return pitches

def plot_pitch(pitches, name):
    # first clear axes and figure
    cla()
    clf()
    # generate lists from pitch objects
    times = [p.time for p in pitches]
    values = [p.pitch for p in pitches]
    # graph pitch
    plot(times, values)
    savefig(name[:-4])
    # show()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: %s <filename> <fft_size> <limit>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    chunk = int(sys.argv[2]) # 1024
    limit = int(sys.argv[3]) # 170 works for me, depends on your F0

    pitches = read_pitch(filename, chunk)
    pitches = filter_pitch(pitches, limit)
    plot_pitch(pitches, filename)

