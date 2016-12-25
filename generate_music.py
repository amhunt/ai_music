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
num_output_phrases = int(sys.argv[1])
input_file_str = sys.argv[2]

stored_data = pickle.load( open(input_file_str, "rb") )
composer_paths = stored_data["composer_paths"]
k = stored_data["k_order"]
markov_map = stored_data["markov_map"]
phrase_bundle = stored_data["phrase_bundle"]
phrase_lengths = stored_data["phrase_lengths"]

# produce new music
empty_score = music21.stream.Part()
(generated_score, generated_phrase_lengths) = generate(num_output_phrases, k, markov_map, empty_score, phrase_bundle)

print("mean phrase length of generated: " + str(mean(generated_phrase_lengths)))
print("std dev of length of generated: " + str(pstdev(generated_phrase_lengths)))

to_store = {
	"k_order": k,
	"generated_score": generated_score,
}

pickle.dump(to_store, open("generated_music_" + str(k) + ".p", "wb"))

# generated_score.show()

