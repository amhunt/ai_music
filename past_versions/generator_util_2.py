
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