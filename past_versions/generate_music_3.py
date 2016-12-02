from music21 import *
import sys
from generator_util_3 import *


def process_notes( notes ):
	i = 0
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
output_length = int(sys.argv[2])
num_scores = int(sys.argv[3])

# compile scores 
palestrina_paths = corpus.getComposer('palestrina')

# add to model
markov_map = {}
i = 0
halfway = False
print("analyzing " + str(num_scores) + " scores")
for score in palestrina_paths[0:num_scores]:
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
	print(i)
	i += 1

# produce new music
first_score_notes = process_score(corpus.parse(palestrina_paths[0]))
first_score_first_notes = first_score_notes[0:k_order]
midi_seed = []
for first_note in first_score_first_notes:
	midi_seed.append(get_note_or_rest(first_note))

empty_score = stream.Part()

generatedScore = generate(midi_seed, output_length, markov_map, empty_score)
generatedScore.show()

