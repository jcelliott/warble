import glob
import sys
from pitch import read_pitch, filter_pitch, plot_pitch

# Create graphs of time vs pitch for all files in the given directory

directory = sys.argv[1]
chunk = int(sys.argv[2])
limit = int(sys.argv[3])

wavs = glob.glob(directory + '/*.wav')
for w in wavs:
    pitches = read_pitch(w, chunk)
    pitches = filter_pitch(pitches, limit)
    plot_pitch(pitches, w)

print "done"
