# parse a MIDI file into vectors of equal length for pitch, rhythm, and velocity
from mido import MidiFile

# only works with monophonic instruments. Returns an matrix
def simple_parse_midi(midifile, trackNum, tempo):
  # mid = MidiFile(midifile) # read in a file
  noteEvents = [] # empty list for note events
  pitches = [] # list for pitches; rests are -1
  velocities = [] # list for velocities of pitches; rests are 127
  rhythms = [] # list of rhythmic units

  for i, msg in enumerate(midifile.tracks[trackNum]):
    if msg.type=='note_on':
      this_rhythm = get_rhythm(msg.time, midifile.ticks_per_beat) * -1 # negative since the last beat was a rest
      # if this_rhythm < -0.05: # eliminate short rests (non-existent rests)
      rhythms.append(this_rhythm)
      pitches.append(-1) # a rest, so no note
      velocities.append(0) # no velocity

    if msg.type=='note_off':
      this_rhythm = get_rhythm(msg.time, midifile.ticks_per_beat) # negative since the last beat was a rest
      rhythms.append(this_rhythm) # remember the duration of the note
      pitches.append(msg.note) # remember the pitch
      velocities.append(msg.velocity) # remember the loudness of that note

  return([pitches, rhythms, velocities])

def get_tempo(midifile):
  for track in midifile.tracks:
    for msg in track:
      if msg.type=='set_tempo':
          return(msg.tempo)

def get_rhythm(time, ticks_per_beat):
    return (time/ticks_per_beat)

def make_ticks(rhythm, ticks_per_beat):
    return(rhythm*ticks_per_beat)

# check key and transpose accordingly
def check_key(mid, desiredKey):
  pass
