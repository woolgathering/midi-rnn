from mido import MidiFile
from utils.midi_funcs import *
from utils.time_series_funcs import *
import numpy as np
from itertools import groupby

# midifile = MidiFile('midi/all_blues_bl.mid')
midifile = MidiFile('midi/MilesDavis_SoWhat_FINAL.mid')
track = midifile.tracks[0]
#
# tempo = get_tempo(mid)
# print(tempo)
#
# parsed = simple_parse_midi(midifile, 0, get_tempo(midifile))
# print(parsed[0])
generated = read_features('midi/data/Generated.txt')


features_to_midi_NORESTS(generated, get_tempo(midifile), midifile.ticks_per_beat, 'midi/data/resynth/fromParsed.mid')


#
# make_time_series(midifile, 0, "./time_series")
#
# time_series = read_time_series("./time_series") # read the time series into memory
# time_signature = {'numerator': time_series.get('numerator'), \
#   'denominator': time_series.get('denominator'), \
#   'clocks_per_click': time_series.get('clocks_per_click'), \
#   'notated_32nd_notes_per_beat': time_series.get('notated_32nd_notes_per_beat'), \
# }
# tempo = time_series.get('tempo')
# ticks_per_beat = time_series.get('ticks_per_beat')
# time_series = time_series.get('time_series')
#
# # time_signature = get_time_signature(midifile)
# time_series_to_midifile(time_series, tempo*2.5, ticks_per_beat, time_signature, "./midi/data/resynth/testMIDI.mid")
#
# # notes = extract_notes_from_time_series(time_series)
# # rhythm = extract_rhythm_from_time_series(time_series)
#
# # time_series_file = open("./time_series", "r") # read the file in
# # time_series = time_series_file.readline() # read in the file; it's just one line
# # time_series = list(map(int, time_series.split(" "))) # split and convert to integers
# # print (rhythm)
