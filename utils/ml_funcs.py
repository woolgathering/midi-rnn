import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import tensorflow as tf

# create and train a model
def make_and_train(data, memory=10):
  raw_data = []
  ini = 0
  end = ini + memory
  while end < len(data):
    raw_data.append(data[ini:end])
    ini = ini + 1
    end = end + 1

  data_y = [e[memory-1] for e in raw_data]
  data_X = [e[:-1] for e in raw_data]

  # reshape X to be [samples, time_steps, features]
  X = np.reshape(data_X, (len(data_X), len(data_X[0]), 1))

  # one hot encode the output variable
  y = np_utils.to_categorical(data_y)
  #y = data_y

  model = Sequential()
  model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
  model.add(Dropout(0.2))
  model.add(LSTM(256))
  model.add(Dropout(0.2))
  model.add(Dense(y.shape[1], activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam')

  print ("Starting training...")
  with tf.device('/gpu:0'):
    #model.fit(X, y, epochs=500, batch_size=128, callbacks=callbacks_list)
    model.fit(X, y, epochs=500, batch_size=32)

  return model

def generate_date(model, length=100):
  generated = []
  start = np.random.randint(0, len(data_X)-1)
  pattern = data_X[start]

  # generate sequence with a random seed
  for i in range(length):
      x = np.reshape(pattern, (1, len(pattern), 1))
      prediction = model.predict(x, verbose=0)
      index = np.argmax(prediction)

      generated.append(index)
      pattern.append(index)
      pattern = pattern[1:len(pattern)]
  print("Generation Completed!")
  return generated
