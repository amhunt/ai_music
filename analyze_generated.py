import music21
import sys
from generator_util import *
from statistics import mean
from statistics import pstdev
import pickle
import matplotlib.pyplot as plt
from analyzor_util import *


###############################################
#               Start of Main                 #
###############################################

print("Music Analysis Begins")
input_file_str = sys.argv[1]

print("loading pickled data...")
print("loading \'stored_data\'...")
stored_data = pickle.load( open(input_file_str, "rb") )
k_order = stored_data["k_order"]
print("loading \'generated_score\'...")
generated_score = stored_data["generated_score"]
print("retrieving generated phrases...")
generated_phrases = get_phrases(generated_score)

print("running analysis...")
intervals = get_detailed_score_intervals(generated_phrases)
interval_map = {}
last_note_map = {}
for detailed_interval in intervals:
	first_note = detailed_interval[0]
	last_note = detailed_interval[1]
	basic_interval = music21.interval.notesToInterval(first_note, last_note)
	semitones = basic_interval.semitones
	interval_map[semitones] = interval_map.get(semitones, 0) + 1

	last_note_str = last_note.nameWithOctave
	last_note_map[last_note_str] = last_note_map.get(last_note_str, 0) + 1

# normalize
for interval, frequency in interval_map.items():
	interval_map[interval] = frequency/len(intervals)*100

# Process data to be plotted
plot_map(interval_map, 'Generated Phrase Ending Tones', 'percent frequency', 'interval')

# ENDING SCALE DEGREES
print("analyzing ending scale degrees")
interval_from_C4_map = {}
c4_note_obj = note.Note('C4')
for pitch, count in last_note_map.items():
	interval = music21.interval.notesToInterval(c4_note_obj, note.Note(pitch)).semitones
	interval_from_C4_map[interval] = count

# converge to one octave
octave_map = {}
for interval, count in interval_from_C4_map.items():
	scale_degree = interval % 12
	octave_map[scale_degree] = octave_map.get(scale_degree, 0) + count

# normalize
for scale_degree, frequency in octave_map.items():
	octave_map[scale_degree] = frequency/len(intervals)*100

print(last_note_map)
plot_map(octave_map, 'Generated Phrase Ending Scale Degrees', '% Frequency', 'Scale Degree')

# PITCH RANGES WITHIN A PHRASE
generated_phrase_ranges = get_pitch_ranges_of_phrase_list(generated_phrases)

phrase_range_map = {}
for phrase_range in generated_phrase_ranges:
	phrase_range_map[phrase_range] = phrase_range_map.get(phrase_range, 0) + 1

# normalize
for phrase_range, frequency in phrase_range_map.items():
	phrase_range_map[phrase_range] = frequency/len(intervals)*100

plot_map(phrase_range_map, 'Generated Phrase Pitch Ranges', '% Frequency', 'Range in Semitones')
