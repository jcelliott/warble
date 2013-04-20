import glob
import sys
from pitch import read_pitch, filter_pitch, plot_pitch
from intonation import detect_intonation, filter_intonation, plot_intonation

# Create graphs of time vs pitch and time vs intonation for all files in the 
# given directory

directory = sys.argv[1]
chunk = int(sys.argv[2])
limit = float(sys.argv[3])
threshold = float(sys.argv[4])
anchor = float(sys.argv[5])

wavs = glob.glob(directory + '/*.wav')
for w in wavs:
    pitches = read_pitch(w, chunk)
    pitches = filter_pitch(pitches, limit)
    plot_pitch(pitches, w)

    intonations = detect_intonation(pitches)
    intonations = filter_intonation(intonations, threshold)
    plot_intonation(intonations, anchor, w)

print "done"
