from music21 import *
import sys
from generator_util import *
from statistics import mean
from statistics import pstdev
import pickle

def process_notes( notes ):

	# first pass for markov
	i = 0
	curr_phrase_length = 0
	curr_phrase_count = 0
	for noteObj in notes:
		if (i > len(notes)-k_order): 
		# handle last notes (wrap-around case)
			curr_k_notes = get_range_of_notes(notes, i, i+k_order-len(notes))
		else:
			curr_k_notes = get_range_of_notes(notes, i, i+k_order)

		if (i >= len(notes)-k_order):
			next_note = get_note_or_rest( notes[i+k_order-len(notes)] )
		else:
			next_note = get_note_or_rest( notes[i+k_order] )

		if noteObj.isRest:
			if curr_phrase_length != 0:
				lengths_of_phrases.append(curr_phrase_length)
				# print("phrase length: " + str(curr_phrase_length))
				complete_phrase = get_range_of_notes(notes, i - curr_phrase_count, i)
				phrase_bundle.append(complete_phrase)
				curr_phrase_length = 0
				curr_phrase_count = 0
		else:
			curr_phrase_length = curr_phrase_length + noteObj.duration.quarterLength
			curr_phrase_count = curr_phrase_count + 1

		curr_k_notes = str(curr_k_notes)
		if (curr_k_notes in markov_map):
			probs = markov_map[curr_k_notes]
			if (next_note in probs):
				probs[next_note] = probs[next_note]+1
			else:
				probs[next_note] = 1
		else:
			new_probs = {}
			new_probs[next_note] = 1
			markov_map[curr_k_notes] = new_probs
		i += 1

###############################################
#               Start of Main                 #
###############################################

print("Music Generation Begins")
k_order = int(sys.argv[1])
num_scores = int(sys.argv[2])

# compile scores 
composer_paths = corpus.getComposer('palestrina')

# add to model
phrase_bundle = []
markov_map = {}
lengths_of_phrases = []
i = 0
halfway = False
print("analyzing " + str(num_scores) + " scores")
for score in composer_paths[0:num_scores]:
	parsed_score = corpus.parse(score)

	## test for opus
	if hasattr(parsed_score, "scores"):
		for part_of_opus in parsed_score.scores:
			## if opus inside of opus, ignore
			if hasattr(part_of_opus, "parts"):
				score_notes = process_score( part_of_opus )
				process_notes(score_notes)
	elif hasattr(parsed_score, "parts"):
		score_notes = process_score( parsed_score )
		process_notes(score_notes)

	if (i > num_scores/2) and not halfway:
		print("halfway done!")
		halfway = True
	print("analyzing score #"+str(i))
	i += 1

print("mean phrase length of input: " + str(mean(lengths_of_phrases)))
print("std dev of length of input: " + str(pstdev(lengths_of_phrases)))
print("num phrases found: " + str(len(phrase_bundle)))

to_store = { 
	"k_order": k_order,
	"num_scores": num_scores,
	"composer_paths": composer_paths,
	"markov_map": markov_map,
	"phrase_bundle": phrase_bundle,
}

pickle.dump(to_store, open("saved_music_" + str(k_order) + ".p", "wb"))

