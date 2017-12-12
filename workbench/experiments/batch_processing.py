# test script
import os
from glob import glob
from utils.midi_funcs import *
from mido import MidiFile

tune = "bas"
paths = glob('midi/projectMIDI/midi/{}/Weimar/*.mid'.format(tune)) # read the filenames from a directory into an array
print (paths)

# you can check if directories exist and if they dont, automatically create them. But for this, this directory needs to exist.
# Let's organize them in the same way Dave and Nakul have organized the midifiles, but in a different directory
output_dir = 'midi/projectMIDI/data/parsed/tunes/{}/'.format(tune) # output directory
# trans = [0 for _ in range(len(paths))] # this MUST be the same size as paths!! Each number is the number of semitones to transpose by

for i, path in enumerate(paths):
  try:
    base = os.path.basename(path) # the filename is the same as the MIDI file. Doesn't have an extension.
    # parsed = os.path.splitext(base)[0]
    midifile = MidiFile(path)
    transposition = get_key(midifile) * -1 # better tranposition

    # function that parses the file. Transpose is a really important argument; we need
    # to ensure that files are in the same 'key' (arguable, but let's not go there...)
    # There's a function that checks the key of the song so you can do transposition programatically
    # but it's probably not much harder to just do it this way since there's not many files.
    # Also, make sure you're doing the correct track in a multitrack MIDI file. For the Jazzomat,
    # this will always be 0 but for the others, you'll have to check. You can do the same thing
    # as the transposition to get different ones for each file if need be.
    parsed = simple_parse_midi(midifile, trackNum=0, tempo=get_tempo(midifile), transpose=transposition)

    out_file = open(output_dir+os.path.splitext(base)[0], 'w') # open a file for writing
    # read through the feature and write them to a file
    for feature in parsed:
      for j, val in enumerate(feature):
        if j==0:
          out_file.write(str(val)) # don't do a space at the start of the line
        else:
          out_file.write(" "+str(val)) # write a space, then the value

      out_file.write('\n') # write a newline. Will result in an empty 4th line at the EOF

    out_file.close # close the file
  except IndexError:
    print ('ERROR: Index out of range. paths = {}, trans = {}'.format(len(paths), len(trans)))
    break

print ('Files were written to {}'.format(output_dir))
