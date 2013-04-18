#!/usr/bin/env python
# find the intonation pattern given a list of pitches

import sys
from math import fabs
from pylab import cla, clf, plot, savefig, show
from pitch import read_pitch, filter_pitch, Pitch


# Given a list of pitches create a list of intonations (using Pitch objects)
# that represent the direction the pitch is heading and store the difference
# between pitches
def detect_intonation(pitches):
    if pitches == None: return None
    last = pitches[0]
    
    # mark each pitch as increasing or decreasing based on the one before it
    for p in pitches:
        if p == last: continue
        if p.pitch > last.pitch:
            p.intonation = 1
        elif last.pitch > p.pitch:
            p.intonation = -1
        last = p

    # add up the pitch change over all sequential pitch changes with the same direction
    last = pitches[0]
    intonations = []
    for p in pitches:
        if p == last: continue
        if p.intonation == last.intonation:
            intonations[-1].pitch += fabs(p.pitch - last.pitch)
        else:
            intonations.append(Pitch(fabs(p.pitch - last.pitch), p.time, p.intonation))
        last = p

    if len(intonations) == 0:
        return None
    return intonations

# Filter out intonations based on some threshold. Pitch changes less then the
# threshold are removed and the data is realigned
def filter_intonation(intonations, threshold):
    if intonations == None: return None
    filters = []

    # remove any intonations that whose pitch change is below the threshold
    for i in intonations:
        if i.pitch < threshold:
            filters.append(i)

    intonations = [i for i in intonations if i not in filters]
    if len(intonations) == 0: return None

    # combine intonations with the same directions after filtering
    last = intonations[0]
    combined_intonations = []
    combined_intonations.append(last)
    for i in intonations:
        if i == last: continue
        if i.intonation == last.intonation:
            combined_intonations[-1].pitch += i.pitch
        else:
            combined_intonations.append(Pitch(i.pitch, i.time, i.intonation))
        last = i

    return combined_intonations

# Plot some reconstructed data points based on the intonation data
# with time (x) and intonation (y) and save it
def plot_intonation(intonations, anchor, name):
    if intonations == None: return
    # first clear axes and figure
    cla()
    clf()

    # reconstruct data since we don't keep concrete pitch data
    data = []
    data.append(Pitch(anchor, 0))
    for i in intonations:
        data.append(Pitch((data[-1].pitch + (i.pitch * i.intonation)), i.time))

    # generate lists from pitch objects
    times = [p.time for p in data]
    values = [p.pitch for p in data]
    # graph pitch
    plot(times, values)
    savefig(name[:-4] + "-int")
    # show()

# Return a string representing the melody of the pitches and describe it using
# the terms 'RISING' and 'FALLING'
def get_melody(intonations):
    if intonations == None: return ""
    melody = ""
    for i in intonations:
        if i.intonation > 0: melody += "RISING "
        elif i.intonation < 0: melody += "FALLING "
    return melody


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: %s <filename> <fft_size> <limit> <threshold>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    chunk = int(sys.argv[2]) # 1024
    limit = int(sys.argv[3]) # 170 works for me, depends on your F0
    threshold = float(sys.argv[4]) # try 15

    pitches = read_pitch(filename, chunk)
    pitches = filter_pitch(pitches, limit)

    intonations = detect_intonation(pitches)
    intonations = filter_intonation(intonations, threshold)
    # print intonations

    # arbitrary starting point for intonation plot since we don't keep concrete pitch data
    anchor = 100 
    plot_intonation(intonations, anchor, filename)

