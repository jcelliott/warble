import glob
import sys
from pitch import read_pitch, filter_pitch, plot_pitch
from intonation import detect_intonation, filter_intonation, get_melody

# Create a text file listing the names and melody patterns of all files in the
# given directory

directory = sys.argv[1]
chunk = int(sys.argv[2])
limit = int(sys.argv[3])
threshold = float(sys.argv[4])

outfile = open(directory + '/intonation.txt', 'w')

wavs = glob.glob(directory + '/*.wav')
for w in wavs:
    pitches = read_pitch(w, chunk)
    pitches = filter_pitch(pitches, limit)

    intonations = detect_intonation(pitches)
    intonations = filter_intonation(intonations, threshold)

    outfile.write("%s:\t%s\n" %(w, get_melody(intonations)))

outfile.close()
print "done"
