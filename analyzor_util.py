import matplotlib.pyplot as plt
import generator_util
import music21
import sys

def plot_map( map, title, xlabel, ylabel ):
	x = []
	y = []
	for key, value in map.items():
		x.append(key)
		y.append(value)
	plt.bar(x, y)
	plt.ylabel(xlabel)
	plt.xlabel(ylabel)
	plt.title(title)
	plt.show()

def plot_pitch_map( map, title, xlabel, ylabel ):
	x = []
	y = []
	x_ticks = []
	i = 0
	for key, value in map.items():
		x.append(i)
		y.append(value)
		x_ticks.append(key)
		i += 1
	print(x_ticks)
	fig, ax = plt.subplots()
	fig.canvas.draw()
	ax.set_xticks(range(len(x_ticks)))
	ax.set_xticklabels(x_ticks)
	plt.bar(x, y)
	plt.ylabel(xlabel)
	plt.xlabel(ylabel)
	plt.title(title)
	plt.show()

def get_score_intervals( generated_score ):
	intervals = []
	i = 0
	curr_phrase_count = 0
	for note_obj in generated_score:
		if note_obj.isRest:
			if curr_phrase_count != 0:
				# deal with phrase
				complete_phrase = generator_util.get_list_of_note_objects(generated_score[(i-curr_phrase_count):i])
				first_note = complete_phrase[0]
				last_note = complete_phrase[len(complete_phrase)-1]
				interval = music21.interval.notesToInterval(first_note, last_note)
				intervals.append(interval)
				curr_phrase_count = 0
		else:
			curr_phrase_count = curr_phrase_count + 1
		i += 1
	return intervals

def get_detailed_score_intervals( generated_phrases ):
	intervals = []
	for phrase in generated_phrases:
		# deal with phrase
		first_note = phrase[0]
		last_note = phrase[len(phrase)-1]
		intervals.append([first_note, last_note])
	return intervals


def get_phrases( generated_score ):
	phrases = []
	i = 0
	curr_phrase_count = 0
	for note_obj in generated_score:
		if note_obj.isRest:
			if curr_phrase_count != 0:
				# deal with phrase
				complete_phrase = generator_util.get_list_of_note_objects(generated_score[(i-curr_phrase_count):i])
				phrases.append(complete_phrase)

				curr_phrase_count = 0
		else:
			curr_phrase_count = curr_phrase_count + 1
		i += 1
	return phrases

def get_pitch_range_of_phrase( phrase ):
	highest_pitch = 0
	lowest_pitch = sys.maxsize
	for note_obj in phrase:
		pitch = note_obj.midi
		if pitch < lowest_pitch:
			lowest_pitch = pitch 
		if pitch > highest_pitch:
			highest_pitch = pitch 

	return (highest_pitch - lowest_pitch)

def get_pitch_ranges_of_phrase_list( phrase_list ):
	ranges = []
	for phrase in phrase_list:
		ranges.append(get_pitch_range_of_phrase(phrase))
	return ranges

def get_list_of_note_objs_from_str( note_str_list ):
	phrase = []
	for note_str in note_str_list:
		new_note_obj = music21.note.Note(note_str.split(':')[1])
		phrase.append(new_note_obj)

	return phrase

def get_phrase_objs_from_str( phrase_str_list ):
	phrase_bundle = []
	for phrase in phrase_str_list:
		phrase_bundle.append(get_list_of_note_objs_from_str(phrase))

	return phrase_bundle


