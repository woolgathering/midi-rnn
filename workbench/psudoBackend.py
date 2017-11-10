### OUR PRETEND BACKEND PROCESS ###
from mido import *

mid = MidiFile() # new MIDI file
track = MidiTrack() # new MIDI track to put notes and rests into
mid.tracks.append(track) # put the newly created track in the newly created file

# assuming we have a list of rhythms that are from the rhythm RNN and a list of notes from the note RNN...
rhythms = myRhythmRNNSet.sample() # get a list of samples
notes = myNoteRNNSet.sample() # get a list of samples
velocities = myVelocityRNNSet.sample()# get a list of samples

## Somewhere here, before iterating, we reconstruct the sequences found by a Factor Oracle. The other thing is that
## this also ensures that we don't have straight up repetitions from the various samples we gave the networks since there's no
## guarentee that the rhtyhm and note sequences are the same length.

## Somewhere here we'd have to solve the interpolating problem. Or maybe before we even poll the networks in the first place. Networks
## feeding networks?? Harsh, how would that look? A separate network for each sample that then feed another network on the same
## musical dimension?

## The iteration is also where we can mess with stuff, like multiplying the time delta by some factor, random or otherwise, so we get
## jacked up rhythms that dont correspond to the harmony or whatever. This would distort the outcome in perhaps interesting ways. We
## could also mess with the note values and see if we can get it out of equal temperament. Or we can force it to play 'out of key'.

## Dave and I also talked about looking at Pygame or something where we can mess with the actual nodes in the network during sampling:
## turning them off at random, randomly adjusting weights, or something else that would give us more interesting, less accurate, or
## "noisy" results. It's also interesting to try to acheive musical results via non-musical means. This could be especially
## interesting if we can do it in realtime.

noteIdx = 0 # something to increment
# iterate
for val in rhythms:
  if val<0:
    # if our val is negative, it gets paired with a note_on event (note on takes place after a rest, generally)
    track.append(Message('note_on', note=notes[noteIdx], velocity=127, time=val*-1)) # set the note and make it positive
  if val>0:
    # if our val is positive, it gets paired with a note_off event of the same note that just passed
    track.append(Message('note_off', note=notes[noteIdx], velocity=velocities[noteIdx], time=val))
    noteIdx += 1 # now we increment

# when we're done with the rhythms, we save. This means we have to be sure the notes outnumber the rhythms, OR that if we run out of notes,
# we poll myNoteRNN again for more notes.
mid.save('new_song.mid')
