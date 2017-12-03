from mido import MidiFile
from utils.midi_funcs import *
import numpy as np
from itertools import groupby

midifile = MidiFile('midi/MilesDavis_SoWhat_FINAL.mid')
track = midifile.tracks[0]
#
# tempo = get_tempo(mid)
# print(tempo)
#
parsed = simple_parse_midi(midifile, 0, get_tempo(midifile))
# print(parsed)
#
# sig = get_key(mid)
# print(sig)

# thisFile = open("./midiFeatures.txt", "w")
# features = ' '.join(str(e) for e in parsed[0])
# thisFile.write(features)
# thisFile.write("\n")
# features = ' '.join(str(e) for e in parsed[1])
# thisFile.write(features)
# thisFile.write("\n")
# features = ' '.join(str(e) for e in parsed[2])
# thisFile.write(features)
# thisFile.close
# print(parsed)

#
# noteEvents = [] # empty list for note events
# pitches = [] # list for pitches; rests are -1
# velocities = [] # list for velocities of pitches; rests are 127
# rhythms = [] # list of rhythmic units
# measure = []
# time_sum = 0
# intervals = []
#
# for msg in track:
#   if msg.type=='note_on':
#     pitches.append(msg.note)
#
# for i, pitch in enumerate(pitches):
#   if i>0:
#     intervals.append(pitches[i] - pitches[i-1])
#
# # print (intervals)
# intervals = get_intervals(parsed[0])
# # print(intervals)
#
# parsed = get_phrases(midifile, 0, get_tempo(midifile))
# for phrase in parsed[0]:
#   print(phrase)
# print(parsed[0])

make_time_series(midifile, 0, "./time_series")

time_series = read_time_series("./time_series")
# tempo = time_series.get('tempo')
# ticks_per_beat = time_series.get('ticks_per_beat')
# time_series = time_series.get('time_series')
#
# time_signature = get_time_signature(midifile)
# time_series_to_midifile(time_series, tempo, ticks_per_beat, "./testMIDI.mid")

# time_series_file = open("./time_series", "r") # read the file in
# time_series = time_series_file.readline() # read in the file; it's just one line
# time_series = list(map(int, time_series.split(" "))) # split and convert to integers
print (time_series)

# [len(list(group)) for key, group in groupby(a)]
