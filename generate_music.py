from music21 import *
import sys
import random

def get_note_or_rest( note ):
	if note.isRest:
		# could try duration.quarterLength as well
		return "rest:"+note.duration.type+':'+note.duration.type
	else:
		return "note:"+note.nameWithOctave+':'+str(note.duration.quarterLength)

def get_range_of_notes( notes, start, end ):
	new_note_list = []
	if end > start: 
		for in_range_note in notes[start:end]:
			new_note_list.append(get_note_or_rest(in_range_note))
	else:
		for in_range_note in notes[start:]:
			new_note_list.append(get_note_or_rest(in_range_note))
		for in_range_note in notes[:end]:
			new_note_list.append(get_note_or_rest(in_range_note))
	return new_note_list


def process_score( score ):
	if len(score.parts.stream()) == 0:
		print("no parts")
		return
	sopPart = score.parts.stream()[0]
	notes = sopPart.flat.notesAndRests
	i=0
	for noteObj in notes:
		if not noteObj.isRest:
			break
		else:
			i+=1

	notes = notes[i:]
	return notes

def process_notes( notes ):
	i=0
	for noteObj in notes:

		if (i > len(notes)-k_order): 
		# handle last notes (wrap-around case)
			curr_k_notes = get_range_of_notes(notes, i, i+k_order-len(notes))
		else:
			curr_k_notes = get_range_of_notes(notes, i, i+k_order)

		if (i >=len(notes)-k_order):
			next_note = get_note_or_rest( notes[i+k_order-len(notes)] )
		else:
			next_note = get_note_or_rest( notes[i+k_order] )

		curr_k_notes = str(curr_k_notes)
		if (curr_k_notes in markovMap):
			probs = markovMap[curr_k_notes]
			if (next_note in probs):
				probs[next_note] = probs[next_note]+1
			else:
				probs[next_note] = 1
		else:
			new_probs = {}
			new_probs[next_note] = 1
			markovMap[curr_k_notes] = new_probs
		i += 1

def get_notes_in_range( notes, start, end ):
	new_note_list = []
	if end > start: 
		for note in notes[start:end]:
			new_note_list.append(note)
	else:
		for note in notes[start:]:
			new_note_list.append(note)
		for note in notes[:end]:
			new_note_list.append(note)
	return new_note_list


def generate(first_k_notes):
	print("generating music")
	i = 0
	generated = []
	curr_notes = get_notes_in_range(first_k_notes,0,len(first_k_notes))
	while (i < output_length):
		# print(i)
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
		# print(generatedNote)
		generatedNoteDetails = generatedNote.split(':')
		if generatedNoteDetails[0] == "rest":
			n = note.Rest(generatedNoteDetails[1])
			n.duration.type = generatedNoteDetails[2]
		else:
			n = note.Note(generatedNoteDetails[1])
			n.duration.quarterLength = float(generatedNoteDetails[2])
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
halfway = False
print("analyzing " + str(num_scores) + " scores")
for score in palestrina_paths[:num_scores]:
	score_notes = process_score( corpus.parse(score) )
	process_notes(score_notes)
	if (i > num_scores/2) and not halfway:
		print("halfway done!")
		halfway = True
	print(i)
	i+=1

# produce new music
first_score_notes = process_score(corpus.parse(palestrina_paths[0]))
first_score_first_notes = first_score_notes[0:k_order]
midi_seed = []
for first_note in first_score_first_notes:
	midi_seed.append(get_note_or_rest(first_note))


generatedScore = generate(midi_seed)
generatedScore.show()




