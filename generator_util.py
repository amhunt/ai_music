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
		return "rest:"+note.duration.type+':'+str(note.duration.quarterLength)
	elif note.isNote:
		return "note:"+note.nameWithOctave+':'+str(note.duration.quarterLength)
	else:
		return "error"

def get_range_of_note_objects( notes, start, end ):
	new_note_list = []
	if end > start: 
		new_note_list = get_list_of_note_objects( notes[start:end] )
	else:
		new_note_list = get_list_of_note_objects( notes[start:].extend(notes[:end]) )
	return new_note_list

def get_list_of_note_objects( notes ):
	return notes

	# THIS WAS PREVENTING ERRORS EARLIER ON BUT IS NOT LIKELY UNNECESSARY (AND SLOW)
	# new_note_list = []
	# for in_range_note in notes:
	# 	new_note_or_rest = in_range_note
	# 	if new_note_or_rest != "error":
	# 		new_note_list.append(new_note_or_rest)
	# return new_note_list

def convert_to_strings( notes ):
	new_note_list = []
	for note_obj in notes:
		new_note_list.append(get_note_or_rest(note_obj))
	return new_note_list

def get_range_of_notes( notes, start, end ):
	return convert_to_strings(get_range_of_note_objects(notes, start, end))

def process_score( score ):
	if len(score.parts.stream()) == 0:
		print("no parts")
		return
	first_part = score.parts.stream()[0]
	notes = first_part.flat.notesAndRests

	## find first non-rest note
	i = 0
	for note_obj in notes:
		if note_obj.isRest:
			i += 1
		else:
			break

	notes = notes[i:]
	return notes

def get_note_length( note_len_str ):
	if "/" in note_len_str:
		fraction = note_len_str.split('/')
		note_length = float(fraction[0]) / float(fraction[1])
	else:
		note_length = float(note_len_str)

	return note_length

def append_phrase_to_score(phrase, curr_score):
	curr_phrase_length = 0
	for generated_note in phrase:
		generated_note_details = generated_note.split(':')
		if generated_note_details[0] == "rest":
			print("WTF")
		n = note.Note(generated_note_details[1])
		curr_note_length = get_note_length(generated_note_details[2])
		n.duration.quarterLength = curr_note_length
		curr_phrase_length = curr_phrase_length + curr_note_length
		curr_score.append(n)
	return (curr_score, curr_phrase_length)

def create_score_from_generated( generated_phrases, curr_score, orig_phrases ):
	i = 0
	generated_lengths_of_phrases = []
	num_phrases_duplicated = 0
	for phrase in generated_phrases:
		complete_phrase = get_notes_in_range(phrase, 0, len(phrase))
		curr_phrase_length = 0

		if complete_phrase in orig_phrases:
			num_phrases_duplicated = num_phrases_duplicated + 1
		else:
			# Un-tab this to save all phrases (not just novel ones!)
			(curr_score, curr_phrase_length) = append_phrase_to_score(complete_phrase, curr_score)

			# append rest at end of each phrase
			new_rest = note.Rest()
			new_rest.duration.quarterLength = 4 - (curr_phrase_length%4)
			curr_score.append(new_rest)

			generated_lengths_of_phrases.append(curr_phrase_length)


	print(str(len(generated_phrases)) + ' phrases produced')
	print(str(len(generated_lengths_of_phrases)) + ' ORIGINAL phrases produced')
	print(str(num_phrases_duplicated) + ' duplicate phrases found and removed')
	return (curr_score, num_phrases_duplicated, generated_lengths_of_phrases)


def generate(num_output_phrases, k, markov_map, curr_score, orig_phrases):
	# print("generating music")
	i = 0
	generated_phrases = []
	curr_phrase_length = 0
	curr_num_phrases = 0
	while curr_num_phrases < num_output_phrases:
		curr_notes = []
		# some phrases are shorter than length k, so avoid them
		curr_notes = random.choice(orig_phrases)[0:k]
		while len(curr_notes) < k:
			curr_notes = random.choice(orig_phrases)[0:k]
			print("too short")

		if (str(curr_notes) not in markov_map):
			print("ERROR: notes not found " + str(curr_notes))
			break
		generated = []
		is_rest = False
		curr_phrase_length = 0
		for start_note in curr_notes:
			generated.append(start_note)
			curr_phrase_length = curr_phrase_length + get_note_length( start_note.split(':')[2] )

		while not is_rest:
			probs = markov_map[str(curr_notes)]
			sum_of_possibilities = 0
			next_note = ""
			for key, value in probs.items():
				sum_of_possibilities = sum_of_possibilities + value

			r = random.uniform(0, sum_of_possibilities)
			upto = 0

			# if curr phrase is long, go to rest if there is one
			# 20 is a good phrase length early cutoff for palestrina phrases
			for key, value in probs.items():
				if curr_phrase_length > 20:
					if key.split(':')[0] == "rest":
						next_note = key
						break
				if upto + value >= r:
					next_note = key
					break
				upto += value

			next_note_parts = next_note.split(':')
			if next_note_parts[0] == "rest":
				is_rest = True
			else:
				generated.append(next_note)
				curr_phrase_length = curr_phrase_length + get_note_length( next_note_parts[2] )
				curr_notes = curr_notes[1:]
				curr_notes.append(next_note)

		generated_phrases.append(generated)
		curr_num_phrases = curr_num_phrases + 1

	# convert to score
	(curr_score, num_phrases_duplicated, generated_lengths_of_phrases) = create_score_from_generated(generated_phrases, curr_score, orig_phrases)

	return (curr_score, generated_lengths_of_phrases)