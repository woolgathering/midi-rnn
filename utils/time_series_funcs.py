# time_series funcs
def make_time_series(midifile, track_num, out_path, transpose=0):
  time_series = [] # an empty list
  this_file = open(out_path, "w") # open a file for writing
  time_signature = get_time_signature(midifile)

  # write a header
  this_file.write(str(get_tempo(midifile))) # write the get_tempo
  this_file.write(" ") # a space

  this_file.write(str(time_signature.get('numerator')))
  this_file.write(" ")
  this_file.write(str(time_signature.get('denominator')))
  this_file.write(" ")
  this_file.write(str(time_signature.get('clocks_per_click')))
  this_file.write(" ")
  this_file.write(str(time_signature.get('notated_32nd_notes_per_beat')))
  this_file.write(" ")
  this_file.write(str(midifile.ticks_per_beat)) # ticks per beat
  this_file.write(" ") # a space
  this_file.write("0 0 0 0") # four zeros

  for track in midifile.tracks[track_num]:
    try:
      for msg in track:
        # it's a rest!
        if msg.type=="note_on":
          # write msg.time number of 'samples'
          for _ in range(msg.time):
            this_file.write(" ") # a space
            this_file.write(str(-1)) # a rest is -1
        # it's a note!
        if msg.type=="note_off":
          for _ in range(msg.time):
            this_file.write(" ") # a space
            this_file.write(str(msg.note+transpose)) # the note number and the transposition
    except TypeError:
      # this is for files that aren't organized into tracks... Like the Jazzomat stuff
      msg = track
      # it's a rest!
      if msg.type=="note_on":
        # write msg.time number of 'samples'
        for _ in range(msg.time):
          this_file.write(" ") # a space
          this_file.write(str(-1)) # a rest is -1
      # it's a note!
      if msg.type=="note_off":
        for _ in range(msg.time):
          this_file.write(" ") # a space
          this_file.write(str(msg.note)) # the note number

  this_file.close # close the file
  return out_path # return the out_path

# read a file of time_series
def read_time_series(filepath):
  time_series_file = open(filepath, "r") # read the file in
  time_series = time_series_file.readline() # read in the file; it's just one line
  time_series = list(map(int, time_series.split(" "))) # split and convert to integers

  tempo = time_series[0] # get the tempo in ticks
  numerator = time_series[1]
  denominator = time_series[2]
  clocks_per_click = time_series[3]
  notated_32nd_notes_per_beat = time_series[4]
  ticks_per_beat = time_series[5] # get the ticks_per_beat

  time_series = time_series[10:] # filter out the header
  time_series_file.close() # close the file
  # return a dict with info
  info = {'tempo': tempo, 'ticks_per_beat': ticks_per_beat, 'time_series': time_series}
  info['numerator'] = numerator
  info['denominator'] = denominator
  info['clocks_per_click'] = clocks_per_click
  info['notated_32nd_notes_per_beat'] = notated_32nd_notes_per_beat
  return info

def normalize_time_series(time_series, clocks_per_click=24):
  # this is an important function! Normalize the time series to a common clocks per click and notated_32nd_notes_per_beat

  notes = extract_notes_from_time_series(time_series)
  rhythms = extract_rhythm_from_time_series(time_series)
  factor = clocks_per_click/24
  tmp_time_series = []

  for i, rhythm in enumerate(rhythms):
    for _ in round(rhythm*factor):
      tmp_time_series.append(notes[i])

  return tmp_time_series

def time_series_to_midifile(time_series, tempo, ticks_per_beat, time_signature, out_path):
  midifile = MidiFile() # create the file
  track = MidiTrack() # create a track
  midifile.tracks.append(track) # append the track to the file
  prev_dur = None

  track.append(MetaMessage('set_tempo', tempo=int(tempo)))
  track.append(MetaMessage('time_signature', numerator=time_signature.get('numerator'), \
   denominator=time_signature.get('denominator'), \
   clocks_per_click=time_signature.get('clocks_per_click'), \
   notated_32nd_notes_per_beat=time_signature.get('notated_32nd_notes_per_beat'), time=0))

  for note, group in groupby(time_series):
    if note < 0: # it's a rest so only remember how long it is
      prev_dur = len(list(group))
    else: # else it's a note
      message = Message('note_on', note=note, velocity=100, time=prev_dur) # note on
      track.append(message)
      message = Message('note_off', note=note, velocity=127, time=len(list(group))) # note off
      track.append(message)
      prev_dur = len(list(group)) # set the prev_dur

  midifile.save(out_path) # save it when we're done

def extract_rhythm_from_time_series(time_series):
  rhythms = []
  for note, group in groupby(time_series):
    if note>=0:
      rhythms.append(len(list(group)))
    else:
      length = len(list(group))
      length = length * -1
      rhythms.append(length) # rests are negative values
  return rhythms

def extract_notes_from_time_series(time_series):
  notes = [note for note, group in groupby(time_series)]
  return notes

def combine_notes_and_rhythm(notes, rhythms):
  time_series = []
  # go through the notes and attach them to rhythms
  for i, note in enumerate(notes):
    try:
      rhythm = rhythms[i]
      if note>0 and rhythm>0:
        for _ in range(rhythm):
          time_series.append(note) # write in the note
      elif rhythm<0:
        for _ in range(rhythm):
          time_series.append(-1) # write in a rest
    except IndexError:
      print ("Too many notes for rhythms. Wrapping up...")

  return time_series
