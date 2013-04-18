import glob
import sys
from pitch import read_pitch, filter_pitch, plot_pitch

chunk = int(sys.argv[1])
limit = int(sys.argv[2])

wavs = glob.glob('data/*.wav')
for w in wavs:
    pitches = read_pitch(w, chunk)
    pitches = filter_pitch(pitches, limit)
    plot_pitch(pitches, w)

print "done"
