from mido import MidiFile
from utils.midi_funcs import *

mid = MidiFile('midi/MilesDavis_SoWhat_FINAL.mid')

tempo = get_tempo(mid)
print(tempo)

parsed = simple_parse_midi(mid, 0, tempo)
print(parsed)
