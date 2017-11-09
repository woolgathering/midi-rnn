from mido import MidiFile

mid = MidiFile('../midi/all_blues_bl.mid') # find yer own file

# get notes in sequence and amplitudes. Each can (should?) be processed independently.
notes = [] # empty list to put the notes into
velocities = [] # empty list for velocities
track = mid.tracks[2] # we'll use the second track (since in my example, it's a monophonic instrument)
for msg in track:
    if msg.type=="note_on":
        notes.append(msg.note) # just get the note on events since it always has a correlate note_off of the same note
        velocities.append(msg.velocity) # remember how loud it was
# print(notes)

# get rhythms
rhythms = []
for msg in track:
    if msg.type=="note_on":
        rest = msg.time * -1
        rhythms.append(rest)
    if msg.type=="note_off":
        noteLength = msg.time
        rhythms.append(noteLength)
# print(rhythms) # list of rhythms in ticks (delta; ticks since last message). Negative values are rests (no sound)
## in other words, negative messages get paired with note_on events if we're creating a new MIDI file message by message.

### Dave and I were thinking that we should use a Factor Oracle on these independently to find sequences. This would allow us to
### more convincingly blend different styles/performers/etc.

### I imagine that converting the ticks to milliseconds or some other value (proportion of beat?) would be easier.
### This can be done later but I think this can give us something to work with. These lists can be saved as CSV files or just used as-is.
### Dave and I were thinking that we should send the RNN (Harsh) the deconstructed musical information - in this case just notes and rhythms
### - and get out whatever the RNN gives us, then do reconstruction of a MIDI file on the backend. This won't be hard with the mido module.
