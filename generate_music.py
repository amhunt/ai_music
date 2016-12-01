import music21
import sys
from generator_util import *
from statistics import mean
from statistics import pstdev
import pickle

###############################################
#               Start of Main                 #
###############################################

print("Music Generation Begins")
output_length = int(sys.argv[1])
input_file_str = sys.argv[2]

stored_data = pickle.load( open(input_file_str, "rb") )
composer_paths = stored_data["composer_paths"]
k_order = stored_data["k_order"]
markov_map = stored_data["markov_map"]
phrase_bundle = stored_data["phrase_bundle"]

# produce new music
first_score_notes = process_score(music21.corpus.parse(composer_paths[0]))
first_score_first_notes = first_score_notes[0:k_order]
midi_seed = []
for first_note in first_score_first_notes:
	midi_seed.append(get_note_or_rest(first_note))

empty_score = music21.stream.Part()

(generatedScore, generated_phrase_lengths) = generate(midi_seed, output_length, markov_map, empty_score, phrase_bundle)

print("mean phrase length of generated: " + str(mean(generated_phrase_lengths)))
print("std dev of length of generated: " + str(pstdev(generated_phrase_lengths)))
# generatedScore.show()

