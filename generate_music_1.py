from music21 import *
import sys
import random

def get_range_of_notes( notes, start, end ):
	new_note_list = []
	if end > start: 
		for in_range_note in notes[start:end]:
			new_note_list.append(in_range_note.midi)
	else:
		for in_range_note in notes[start:]:
			new_note_list.append(in_range_note.midi)
		for in_range_note in notes[:end]:
			new_note_list.append(in_range_note.midi)
	return new_note_list



def process_score( score ):
	if len(score.parts.stream()) == 0:
		print("no parts")
		return
	sopPart = score.parts.stream()[0]
	notes = sopPart.flat.notes
	i = 0

	for noteObj in notes:
		i+=1
	i=0
	for noteObj in notes:
		# last notes
		if (i > len(notes)-k_order):
			curr_k_notes = get_range_of_notes(notes, i, i+k_order-len(notes))
		else:
			curr_k_notes = get_range_of_notes(notes, i, i+k_order)

		if (i >=len(notes)-k_order):
			next_note = notes[i+k_order-len(notes)].midi
		else:
			next_note = notes[i+k_order].midi

		curr_k_notes_str = str(curr_k_notes)
		if (curr_k_notes_str in markovMap):
			probs = markovMap[curr_k_notes_str]
			if (next_note in probs):
				probs[next_note] = probs[next_note]+1
			else:
				probs[next_note] = 1
		else:
			new_probs = {}
			new_probs[next_note] = 1
			markovMap[curr_k_notes_str] = new_probs
		i += 1

def get_midis_in_range( midis, start, end ):
	new_note_list = []
	if end > start: 
		for note in midis[start:end]:
			new_note_list.append(note)
	else:
		for note in midis[start:]:
			new_note_list.append(note)
		for note in midis[:end]:
			new_note_list.append(note)
	return new_note_list


def generate(first_k_notes):
	print(":::generated music:::")
	i = 0
	generated = []
	curr_notes = get_midis_in_range(first_k_notes,0,len(first_k_notes))
	while (i < output_length):
		if (str(curr_notes) not in markovMap):
			print("ERROR: " + str(curr_notes))
			break

		probs = markovMap[str(curr_notes)]
		sumOfPossibilities = 0
		next_note = ""
		for key, value in probs.items():
			sumOfPossibilities = sumOfPossibilities + value
		r = random.uniform(0, sumOfPossibilities)
		upto = 0
		for key, value in probs.items():
			if upto + value >= r:
				next_note = key
				break
			upto += value

		generated.append(next_note)
		curr_notes = curr_notes[1:]
		curr_notes.append(next_note)
		i = i+1

	# convert to score
	p1 = stream.Part()
	for generatedNote in generated:
		n = note.Note(generatedNote)
		p1.append(n)
	return p1

print("Music Generation Begins")
k_order = int(sys.argv[1])
output_length = int(sys.argv[2])
num_scores = int(sys.argv[3])

# compile scores
palestrina_paths = corpus.getComposer('palestrina')

# add to model
markovMap = {}
i = 0
for score in palestrina_paths[:num_scores]:
	print("analysizing score #" + str(i))
	process_score( corpus.parse(score) )
	i+=1

# produce new music
first_score_notes = corpus.parse(palestrina_paths[0]).parts.stream()[0].flat.notes[0:k_order]
midi_seed = []
for first_note in first_score_notes:
	midi_seed.append(first_note.midi)
generatedScore = generate(midi_seed)
generatedScore.show()




