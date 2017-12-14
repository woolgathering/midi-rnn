import os
from glob import glob
from utils.ml_funcs import *
from utils.midi_funcs import *

players = ["CharlieParker"]
memory = 20 # changed below

for player in players:
  paths = glob('/home/jlsundst/midi-rnn/midi/projectMIDI/data/parsed/players/{}/*'.format(player))
  notes = []
  rhythms = []
  velocities = []

  for path in paths:
    name = os.path.basename(path)
    these_notes, these_rhythms, these_velocities = list(parseMatrixFromFile(path))
    # these_notes = get_intervals(these_notes) # get intervals instead

    notes = notes + these_notes
    rhythms = rhythms + these_rhythms
    velocities = velocities + these_velocities

  print ("Training on {}".format(player))

  print ("Training notes")
  #memory = int(len(notes)*0.012)
  try:
    checkpoint_path = '/home/jlsundst/midi-rnn/midi/projectMIDI/models/checkpoints/{}/notes/'.format(player)
    os.mkdir(checkpoint_path)
  except:
    pass
  note_model = make_and_train(notes, memory, checkpoint_path)
  note_model.save('/home/jlsundst/midi-rnn/midi/projectMIDI/models/{}_notes.h5'.format(player))
  print ("Note model saved!")
  del note_model

  print ("Training rhythms")
  #memory = int(len(rhythms)*0.012)
  try:
    checkpoint_path = '/home/jlsundst/midi-rnn/midi/projectMIDI/models/checkpoints/{}/rhythms/'.format(player)
    os.mkdir(checkpoint_path)
  except:
    pass
  rhythm_model = make_and_train(rhythms, memory, checkpoint_path)
  rhythm_model.save('/home/jlsundst/midi-rnn/midi/projectMIDI/models/{}_rhythms.h5'.format(player))
  print ("Rhythm model saved!")
  del rhythm_model

  print ("Training velocities")
  #memory = int(len(velocities)*0.012)
  try:
    checkpoint_path = '/home/jlsundst/midi-rnn/midi/projectMIDI/models/checkpoints/{}/velocities/'.format(player)
    os.mkdir(checkpoint_path)
  except:
    pass
  velocity_model = make_and_train(velocities, memory, checkpoint_path)
  velocity_model.save('/home/jlsundst/midi-rnn/midi/projectMIDI/models/{}_velocities.h5'.format(player))
  print ("Velocity model saved~")
  del velocity_model
