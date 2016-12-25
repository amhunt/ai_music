import music21
import sys
from generator_util import *
from statistics import mean
from statistics import pstdev
import pickle
from analyzor_util import *

###############################################
#               Start of Main                 #
###############################################

print("Music Generation Begins")
input_file_str = sys.argv[1]

stored_data = pickle.load( open(input_file_str, "rb") )
composer_paths = stored_data["composer_paths"]
k_order = stored_data["k_order"]
markov_map = stored_data["markov_map"]
phrase_bundle = stored_data["phrase_bundle"]
intervals = stored_data["intervals"]

interval_map = {}

for interval in intervals:
	semitones = interval.semitones
	if semitones in interval_map:
		interval_map[semitones] += 1
	else:
		interval_map[semitones] = 1

# Process data to be plotted
print(interval_map)
plot_interval_map(interval_map)
