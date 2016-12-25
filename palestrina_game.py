import random
import music21
from generator_util import *
import sys
import pickle
from time import sleep

sleep(1)
print("Welcome to the Palestrina game!")
sleep(1)
print("this will test how well you can tell the difference " \
	"between actual palestrina phrases and AI generated original ones")
sleep(1)
print("just type \"q\" at any time to end the game")
sleep(1)
print("enjoy!")
input_file_str = sys.argv[1]

stored_data = pickle.load( open(input_file_str, "rb") )
composer_paths = stored_data["composer_paths"]
k = stored_data["k_order"]
markov_map = stored_data["markov_map"]
phrase_bundle = stored_data["phrase_bundle"]
phrase_lengths = stored_data["phrase_lengths"]

options = ["palestrina", "generated"]

# produce new music
num_correct = 0
num_answered = 0
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
			num_correct += 1
		else:
			print("incorrect\n")
	elif ans == "n":
		if score_type == "generated":
			print("correct!\n")
			num_correct += 1
		else:
			print("incorrect\n")
	elif ans == "q":
		print("you answered " + str(num_correct) + " correctly out of " \
			+ str(num_answered) + " total questions")
		break
	else:
		print("not a valid response - answer marked incorrect")
	num_answered += 1

