import numpy as np
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import tensorflow as tf
from glob import glob
from utils.ml_funcs import *

paths = glob('midi/projectMIDI/data/parsed/players/*/*')
memory = 20

for path in paths:
  name = os.path.basename(path)
  notes, rhythms, velocities = list(parseMatrixFromFile(path))

  print ("Training on {}".format(base))

  print ("Training notes")
  note_model = make_and_train(notes, memory)
  print ("Training rhythms")
  rhythm_model = make_and_train(rhythms, memory)
  print ("Training velocities")
  velocity_model = make_and_train(velocities, memory)

  note_model.save('midi/projectMIDI/models/{}_notes.h5'.format(name))
  del note_model
  rhythm_model.save('midi/projectMIDI/models/{}_rhythms.h5'.format(name))
  del rhythm_model
  velocity_model.save('midi/projectMIDI/models/{}_velocities.h5'.format(name))
  del velocity_model
