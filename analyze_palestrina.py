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

print("Analysis of Palestrina Corpus Beginning...")
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
	interval_map[semitones] = interval_map.get(semitones, 0) + 1

ending_notes = {}
for phrase_str in phrase_bundle:
	ending_note = phrase_str[len(phrase_str)-1].split(":")[1]
	ending_notes[ending_note] = ending_notes.get(ending_note, 0) + 1

interval_from_C4_map = {}
c4_note_obj = note.Note('C4')
for pitch, count in ending_notes.items():
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

print(ending_notes)
plot_map(octave_map, 'Palestrina Phrase Ending Scale Degrees', '% Frequency', 'Scale Degree')

# normalize
for interval, frequency in interval_map.items():
	interval_map[interval] = frequency/len(intervals)*100

# Process data to be plotted
plot_map(interval_map, 'Palestrina Phrase Ending Tones', '% Frequency', 'Interval in Semitones')

# PITCH RANGES
phrase_object_bundle = get_phrase_objs_from_str(phrase_bundle)
pal_phrase_ranges = get_pitch_ranges_of_phrase_list(phrase_object_bundle)

phrase_range_map = {}
for phrase_range in pal_phrase_ranges:
	phrase_range_map[phrase_range] = phrase_range_map.get(phrase_range, 0) + 1

# normalize
for phrase_range, frequency in phrase_range_map.items():
	phrase_range_map[phrase_range] = frequency/len(intervals)*100

plot_map(phrase_range_map, 'Palestrina Phrase Pitch Ranges', '% Frequency', 'Range in Semitones')

