# parse a MIDI file into vectors of equal length for pitch, rhythm, and velocity
from mido import Message, MidiFile, MidiTrack, MetaMessage
from itertools import groupby
import numpy as np

# only works with monophonic instruments. Returns an matrix
def simple_parse_midi(midifile, trackNum, tempo, transpose=0):
  # mid = MidiFile(midifile) # read in a file
  pitches = [] # list for pitches; rests are -1
  velocities = [] # list for velocities of pitches; rests are 127
  rhythms = [] # list of rhythmic units

  for i, msg in enumerate(midifile.tracks[trackNum]):
    if msg.type=='note_on':
      this_rhythm = get_rhythm(msg.time, midifile.ticks_per_beat) * -1 # negative since the last beat was a rest
      # if this_rhythm < -0.05: # eliminate short rests (non-existent rests)
      rhythms.append(this_rhythm)
      pitches.append(-1) # a rest, so no note
      velocities.append(127) # no velocity

    if msg.type=='note_off':
      this_rhythm = get_rhythm(msg.time, midifile.ticks_per_beat) # negative since the last beat was a rest
      rhythms.append(this_rhythm) # remember the duration of the note
      pitches.append(msg.note+transpose) # remember the pitch
      velocities.append(msg.velocity) # remember the loudness of that note

  return([pitches, rhythms, velocities])

def read_features(path):
  this_file = open(path, "r") # open the file
  notes = this_file.readline() # read a line
  rhythms = this_file.readline() # read a line
  velocities = this_file.readline() # read a line
  this_file.close() # close it

  notes = list(map(int, notes.split(" "))) # make into a list of integers
  rhythms = list(map(int, rhythms.split(" "))) # make into a list of integers
  velocities = list(map(int, velocities.split(" "))) # make into a list of integers
  return [notes, rhythms, velocities]

def features_to_midi(features, tempo, ticks_per_beat, out_path):
  # get the features
  notes = features[0]
  rhythms = features[1]
  velocities = features[2]

  midifile = MidiFile(ticks_per_beat=ticks_per_beat) # create the file
  track = MidiTrack() # create a track
  midifile.tracks.append(track) # append the track to the file
  track.append(MetaMessage('set_tempo', tempo=int(tempo))) # set the tempo

  for i, note in enumerate(notes):
    try:
      if note!=-1:
        ticks = round(make_ticks(rhythms[i], ticks_per_beat)) # get the delta time
        message = Message('note_off', note=prev_note, velocity=127, time=ticks) # note off
        track.append(message) # attach the message to the track
      else:
        ticks = abs(round(make_ticks(rhythms[i], ticks_per_beat))) # get the delta time
        message = Message('note_on', note=notes[i+1], velocity=velocities[i], time=ticks) # note on
        track.append(message) # attach the message to the track
        prev_note = notes[i+1] # remember this note
    except IndexError:
      print ("Error: Check matrix dimensions. Too many notes.")

  midifile.save(out_path) # save the file
  return out_path

# the size of the array returned is always the number of notes - 1
def get_intervals(pitches):
  intervals = []
  no_rests = []
  for pitch in pitches:
    if pitch>0:
      no_rests.append(pitch)
  for i, pitch in enumerate(no_rests):
    if i>0:
      intervals.append(no_rests[i] - no_rests[i-1])
  return (intervals)

# trying to make phrases
def get_phrases(midifile, trackNum, tempo):
  pitches = np.array([]) # list for pitches; rests are -1
  velocities = [] # list for velocities of pitches; rests are 127
  rhythms = [] # list of rhythmic units
  phrase = np.array([]) # an empty phrase

  for i, msg in enumerate(midifile.tracks[trackNum]):
    if msg.type=='note_on':
      this_rhythm = get_rhythm(msg.time, midifile.ticks_per_beat) * -1 # negative since the last beat was a rest
      if this_rhythm < -0.1: # eliminate short rests (non-existent rests)
        rhythms.append(this_rhythm)
        # phrase.append(-1) # a rest, so no note but it's in our phrase
        np.append(phrase, [-1])
        velocities.append(0) # no velocity
      if this_rhythm < -3:
        # else it's a long rest so we make a new phrase and add the old one to our pitches
        # pitches.append(phrase)
        np.append(pitches, phrase.flatten())
        phrase = np.array([])

    if msg.type=='note_off':
      this_rhythm = get_rhythm(msg.time, midifile.ticks_per_beat) # negative since the last beat was a rest
      rhythms.append(this_rhythm) # remember the duration of the note
      # phrase.append(msg.note) # remember the pitch
      np.append(phrase, [msg.note])
      velocities.append(msg.velocity) # remember the loudness of that note

    print(phrase)

  # pitches.append(phrase) # make sure we append the last phrase (double check that we didn't already)
  np.append(pitches, phrase.flatten())

  # shape = (len(pitches), len(max(pitches,key=len)))
  # pitches = [np.array(phrase) for phrase in pitches]
  # pitches = np.array(pitches)
  # sigma = np.diag(pitches)
  # sigma.resize(shape)

  # zeros = np.zeros(shape, dtype=np.int32)
  # zeros[:sigma.shape[0], :sigma.shape[1]] = sigma
  # pitches = sigma.asarray

  return([pitches, rhythms, velocities])

def get_tempo(midifile):
  for track in midifile.tracks:
    for msg in track:
      if msg.type=='set_tempo':
          return(msg.tempo)

def get_rhythm(time, ticks_per_beat):
    return (time/ticks_per_beat) # beat is 16th notes???

def make_ticks(rhythm, ticks_per_beat):
    return(rhythm*ticks_per_beat)

def get_time_signature(midifile):
  for track in midifile.tracks:
    for msg in track:
      if msg.type=='time_signature':
        return {'numerator': msg.numerator, 'denominator': msg.denominator, 'clocks_per_click': msg.clocks_per_click, 'notated_32nd_notes_per_beat': msg.notated_32nd_notes_per_beat}

# check key
def get_key(midifile):
  for track in midifile.tracks:
    for msg in track:
      if msg.type=='key_signature':
        if msg.key=='C':
          key = 0
        elif msg.key=='C#':
          key = 1
        elif msg.key=='D':
          key = 2
        elif msg.key=='D#':
          key = 3
        elif msg.key=='E':
          key = 4
        elif msg.key=='F':
          key = 5
        elif msg.key=='F#':
          key = 6
        elif msg.key=='G':
          key = 7
        elif msg.key=='Ab':
          key = 8
        elif msg.key=='A':
          key = 9
        elif msg.key=='A#':
          key = 10
        else:
          key = 11
    return (key) # return the key
