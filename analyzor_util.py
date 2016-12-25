import matplotlib.pyplot as plt
import generator_util
import music21

def plot_interval_map( interval_map ):
	x = []
	y = []
	for key, value in interval_map.items():
		x.append(key)
		y.append(value)

	plt.bar(x, y)
	plt.ylabel('num_instances')

	plt.xlabel('semitones_away_from_beginning')
	plt.show()


def get_score_intervals( generated_score ):
	intervals = []
	i = 0
	curr_phrase_length = 0
	curr_phrase_count = 0
	for note_obj in generated_score:
		if note_obj.isRest:
			if curr_phrase_count != 0:
				# deal with phrase
				complete_phrase = generator_util.get_range_of_note_objects(generated_score, i - curr_phrase_count, i)
				first_note = complete_phrase[0]
				last_note = complete_phrase[len(complete_phrase)-1]
				interval = music21.interval.notesToInterval(first_note, last_note)
				intervals.append(interval)

				curr_phrase_length = 0
				curr_phrase_count = 0
		else:
			curr_phrase_count = curr_phrase_count + 1

		i += 1
	return intervals