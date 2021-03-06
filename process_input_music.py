from music21 import *
import sys
from generator_util import *
from statistics import mean
from statistics import pstdev
import pickle
import music21

def process_notes( notes ):

	# pass for markov
	i = 0
	curr_phrase_length = 0
	curr_phrase_count = 0
	for note_obj in notes:
		if (i > len(notes)-k_order): 
		# handle last notes (wrap-around case)
			curr_k_notes = get_range_of_notes(notes, i, i+k_order-len(notes))
		else:
			curr_k_notes = get_range_of_notes(notes, i, i+k_order)

		if (i >= len(notes)-k_order):
			next_note = get_note_or_rest( notes[i+k_order-len(notes)] )
		else:
			next_note = get_note_or_rest( notes[i+k_order] )

		if note_obj.isRest:
			if curr_phrase_length != 0:

				# deal with phrase
				complete_phrase = get_range_of_note_objects(notes, i - curr_phrase_count, i)
				first_note = complete_phrase[0]
				last_note = complete_phrase[len(complete_phrase)-1]
				interval = music21.interval.notesToInterval(first_note, last_note)
				intervals.append(interval)

				phrase_lengths.append(curr_phrase_length)
				complete_phrase_str_list = convert_to_strings(complete_phrase)
				phrase_bundle.append(complete_phrase_str_list)
				curr_phrase_length = 0
				curr_phrase_count = 0
		else:
			if curr_phrase_count == 0:
				first_note = note_obj
			curr_phrase_length = curr_phrase_length + note_obj.duration.quarterLength
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
phrase_lengths = []
intervals = []
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

print("mean phrase length of input: " + str(mean(phrase_lengths)))
print("std dev of length of input: " + str(pstdev(phrase_lengths)))
print("num phrases found: " + str(len(phrase_bundle)))

to_store = {
	"k_order": k_order,
	"num_scores": num_scores,
	"composer_paths": composer_paths,
	"markov_map": markov_map,
	"phrase_bundle": phrase_bundle,
	"phrase_lengths": phrase_lengths,
	"intervals": intervals,
}

pickle.dump(to_store, open("saved_music_" + str(k_order) + ".p", "wb"))

