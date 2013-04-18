#!/usr/bin/env python
# Read in a wav file, find the pitches, and plot them

import sys
import os.path
from pylab import *
from aubio import source, pitch


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
    times = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        cur_pitch = pitch_o(samples)[0]
        # print "%f %f" % (total_frames / float(samplerate), pitch)
        #pitches += [pitches]
        pitches.append(cur_pitch)
        times.append(total_frames / float(samplerate))
        total_frames += read
        if read < hop_s: break

    # print pitches
    return pitches, times

def filter_pitch(pitches, times, limit):
    # filter out values that are too high
    filters = {}
    # remove last data point
    # filters[times[-1]] = pitches [-1]

    for i in range(len(pitches)):
        if pitches[i] > limit or pitches[i] == 0:
            filters[times[i]] = pitches[i]

    for t, p in filters.items():
        times.remove(t)
        pitches.remove(p)

    return pitches, times

def plot_pitch(pitches, times, name):
    # first clear axes and figure
    cla()
    clf()
    # graph pitch
    plot(times, pitches)
    savefig(name[:-4])
    # show()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: %s <filename> <fft_size> <limit>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    chunk = int(sys.argv[2]) # 1024
    limit = int(sys.argv[3]) # 170 works for me, depends on your F0

    pitches, times = read_pitch(filename, chunk)
    pitches, times = filter_pitches(pitches, times, limit)
    plot_pitch(pitches, times, filename)

