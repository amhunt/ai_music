import random
import music21
from generator_util import *
import sys
import pickle

print("Welcome to the Palestrina game!")
input_file_str = sys.argv[1]

stored_data = pickle.load( open(input_file_str, "rb") )
composer_paths = stored_data["composer_paths"]
k = stored_data["k_order"]
markov_map = stored_data["markov_map"]
phrase_bundle = stored_data["phrase_bundle"]
phrase_lengths = stored_data["phrase_lengths"]

options = ["palestrina", "generated"]

# produce new music
while True:
	score_type = random.choice(options)
	empty_score = music21.stream.Part()
	if score_type == "palestrina":
		palestrina_phrase = random.choice(phrase_bundle)
		(generated_score, _) = append_phrase_to_score(palestrina_phrase, empty_score)
	else:		
		(generated_score, generated_phrase_lengths) = generate(1, k, markov_map, empty_score, phrase_bundle)
	generated_score.show()

	ans = input('is this palestrina?\n')
	if ans == "y":
		if score_type == "palestrina":
			print("correct!\n")
		else:
			print("incorrect\n")
	else:
		if score_type == "generated":
			print("correct!\n")
		else:
			print("incorrect\n")
