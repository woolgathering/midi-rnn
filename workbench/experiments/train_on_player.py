import numpy as np
import os
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils
# import tensorflow as tf
from glob import glob
from utils.ml_funcs import *

players = ["MilesDavis", "JohnColtrane", "OrnetteColeman", "CharlieParker"]
memory = 10

for player in players:
  paths = glob('midi/projectMIDI/data/parsed/players/{}/*'.format(player))
  notes = []
  rhythms = []
  velocities = []

  for path in paths:
    name = os.path.basename(path)
    these_notes, these_rhythms, these_velocities = list(parseMatrixFromFile(path))

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

  note_model.save('midi/projectMIDI/models/{}_notes.h5'.format(player))
  del note_model
  rhythm_model.save('midi/projectMIDI/models/{}_rhythms.h5'.format(player))
  del rhythm_model
  velocity_model.save('midi/projectMIDI/models/{}_velocities.h5'.format(player))
  del velocity_model
