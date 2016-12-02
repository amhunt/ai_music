import random
from music21 import note

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
	
def get_note_or_rest( note ):
	if note.isRest:
		# could try duration.quarterLength as well
		return "rest:"+note.duration.type+':'+note.duration.type
	elif note.isNote:
		return "note:"+note.nameWithOctave+':'+str(note.duration.quarterLength)
	else:
		return "error"

def get_range_of_notes( notes, start, end ):
	new_note_list = []
	if end > start: 
		for in_range_note in notes[start:end]:
			new_note_or_rest = get_note_or_rest(in_range_note)
			if new_note_or_rest != "error":
				new_note_list.append(new_note_or_rest)
	else:
		for in_range_note in notes[start:]:
			new_note_or_rest = get_note_or_rest(in_range_note)
			if new_note_or_rest != "error":
				new_note_list.append(new_note_or_rest)
		for in_range_note in notes[:end]:
			new_note_or_rest = get_note_or_rest(in_range_note)
			if new_note_or_rest != "error":
				new_note_list.append(new_note_or_rest)
	return new_note_list

def process_score( score ):
	if len(score.parts.stream()) == 0:
		print("no parts")
		return
	sopPart = score.parts.stream()[0]
	notes = sopPart.flat.notesAndRests

	## find first non-rest note
	i = 0
	for noteObj in notes:
		if noteObj.isRest:
			i += 1
		else:
			break

	notes = notes[i:]
	return notes

def generate(first_k_notes, output_length, markov_map, curr_score):
	print("generating music")
	i = 0
	generated = []
	curr_notes = get_notes_in_range(first_k_notes,0,len(first_k_notes))
	while (i < output_length):
		# print(i)
		if (str(curr_notes) not in markov_map):
			print("ERROR: " + str(curr_notes))
			break

		probs = markov_map[str(curr_notes)]
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
	for generatedNote in generated:
		# print(generatedNote)
		generatedNoteDetails = generatedNote.split(':')
		if generatedNoteDetails[0] == "rest":
			n = note.Rest(generatedNoteDetails[1])
			n.duration.type = generatedNoteDetails[2]
		else:
			n = note.Note(generatedNoteDetails[1])
			n.duration.quarterLength = float(generatedNoteDetails[2])
		curr_score.append(n)
	return curr_score