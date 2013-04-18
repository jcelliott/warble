#!/usr/bin/env python
# find the intonation pattern given a list of pitches

import sys
from pitch import read_pitch, filter_pitch

def detect_intonation(pitches):
    last = pitches[0]
    directions = []
    
    for i in range(len(pitches))[1:]: # start on the second data point
        if pitches[i].pitch > last.pitch:
            directions.append(1)
        # elif pitches[i] == last:
            # should get a 0 if they are close,
            # if abs(pitches[i] - last) < some_threshold
            # directions.append(0)
        else:
            directions.append(-1)
        last = pitches[i]

    return directions


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: %s <filename> <fft_size> <limit>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    chunk = int(sys.argv[2]) # 1024
    limit = int(sys.argv[3]) # 170 works for me, depends on your F0

    pitches = read_pitch(filename, chunk)
    pitches = filter_pitch(pitches, limit)

    intonation = detect_intonation(pitches)
    print intonation
