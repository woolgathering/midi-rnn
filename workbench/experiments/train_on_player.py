import numpy as np
import os
from glob import glob
from utils.ml_funcs import *
from utils.midi_funcs import *

players = ["MilesDavis", "JohnColtrane", "OrnetteColeman", "CharlieParker"]
memory = 15

for player in players:
  paths = glob('/home/roger/Documents/work/206_machineLearning/midi_rnn/midi/projectMIDI/data/parsed/players/{}/*'.format
  notes = []
  rhythms = []
  velocities = []

  for path in paths:
    name = os.path.basename(path)
    these_notes, these_rhythms, these_velocities = list(parseMatrixFromFile(path))
    these_notes = get_intervals(these_notes) # get intervals instead

    notes = notes + these_notes
    rhythms = rhythms + these_rhythms
    velocities = velocities + these_velocities

  print ("Training on {}".format(player))

  print ("Training notes")
  note_model = make_and_train(notes, memory)
  print ("Training rhythms")
  rhythm_model = make_and_train(rhythms, memory)
  print ("Training velocities")
  velocity_model = make_and_train(velocities, memory)

  note_model.save('/home/roger/Documents/work/206_machineLearning/midi_rnn/midi/projectMIDI/models/{}_notes.h5'.format(player))
  del note_model
  rhythm_model.save('/home/roger/Documents/work/206_machineLearning/midi_rnn/midi/projectMIDI/models/{}_rhythms.h5'.format(player))
  del rhythm_model
  velocity_model.save('/home/roger/Documents/work/206_machineLearning/midi_rnn/midi/projectMIDI/models/{}_velocities.h5'.format(player))
  del velocity_model
