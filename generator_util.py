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
		return "rest:"+note.duration.type+':'+str(note.duration.quarterLength)
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

def generate(first_k_notes, output_length, markov_map, curr_score, orig_phrases):
	print("generating music")
	i = 0
	generated = []
	curr_notes = get_notes_in_range(first_k_notes,0,len(first_k_notes))
	curr_phrase_length = 0
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

		# if curr phrase is long, go to rest if there is one
		is_found = False
		if curr_phrase_length > 15:
			for key, value in probs.items():
					if key.split(':')[0] == "rest":
						next_note = key
						is_found = True
						break

		if not is_found:
			for key, value in probs.items():
				if upto + value >= r:
					next_note = key
					break
				upto += value

		generated.append(next_note)

		next_note_parts = next_note.split(':')
		if next_note_parts[0] == "rest":
			curr_phrase_length = 0
		else:
			curr_phrase_length = curr_phrase_length + float(next_note_parts[2])

		curr_notes = curr_notes[1:]
		curr_notes.append(next_note)
		i = i+1

	generated_lengths_of_phrases = []
	curr_phrase_length = 0
	curr_phrase_count = 0
	
	# convert to score
	i = 0
	num_phrases_duplicated = 0
	for generatedNote in generated:
		generatedNoteDetails = generatedNote.split(':')
		if generatedNoteDetails[0] == "rest":
			n = note.Rest(generatedNoteDetails[1])
			n.duration.quarterLength = float(generatedNoteDetails[2])
			if curr_phrase_length != 0:
				generated_lengths_of_phrases.append(curr_phrase_length)
				complete_phrase = get_notes_in_range(generated, i - curr_phrase_count, i)
				print(complete_phrase)
				if complete_phrase in orig_phrases:
					print("duplicate phrase found")
					num_phrases_duplicated = num_phrases_duplicated + 1

				curr_phrase_length = 0
				curr_phrase_count = 0
		else:
			n = note.Note(generatedNoteDetails[1])
			if "/" in generatedNoteDetails[2]:
				fraction = generatedNoteDetails[2].split('/')
				curr_note_length = float(fraction[0]) / float(fraction[1])
			else:
				curr_note_length = float(generatedNoteDetails[2])
			n.duration.quarterLength = curr_note_length
			curr_phrase_length = curr_phrase_length + curr_note_length
			curr_phrase_count = curr_phrase_count + 1
		curr_score.append(n)
		i = i + 1
	print("num phrases created: " + str(len(generated_lengths_of_phrases)))
	print("num duplicate phrases created: " + str(num_phrases_duplicated))
	return (curr_score, generated_lengths_of_phrases)