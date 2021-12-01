"""
This file is used to train the neural network.
It's not needed for the user. It only needs to be ran once.

"""

import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import re
from tensorflow import keras
import pandas as pd
from inspect import getsourcefile
from os.path import abspath
import os
import sys

# Small utility to get the absolute path to the current module.
path_to_datasets = abspath(getsourcefile(lambda: 0))
path_to_datasets = os.path.join(path_to_datasets, '../../../training_datasets')
path_to_datasets = os.path.normpath(path_to_datasets)

# Loading the datasets

# for matrix data, first column is id, second column is rumor indicator 1 or -1,
# other columns are words value is 1 contain or 0 does not contain
"""
matrix1 = pd.read_csv(path_to_datasets+'/matrix.csv')
matrix2 = pd.read_csv(path_to_datasets+'/sample-matrix.csv')

# retrieving the text of each row using the structure of the matrix
header1 = list(matrix1.columns)
header1.remove('id')
header1.remove('isRumor')
matrix1["content"] = matrix1["id"]

for i in range(len(matrix1)):
    matrix1["content"][i] = ""
    for j in header1:
        if matrix1[j][i] == 1:
            matrix1["content"][i] = matrix1["content"][i] + " "+j

header2 = list(matrix2.columns)
header2.remove('id')
header2.remove('isRumor')
matrix2["content"] = matrix2["id"]

for i in range(len(matrix2)):
    matrix2["content"][i] = ""
    for j in header2:
        if matrix2[j][i] == 1:
            matrix2["content"][i] = matrix2["content"][i] + " "+j
"""

fake1 = pd.read_csv(path_to_datasets+'/pin.txt', delimiter=";")
fake2 = pd.read_csv(path_to_datasets+'/randomtweets3.txt', delimiter=",")
fake3 = pd.read_csv(path_to_datasets+'/randomtweets4.txt', delimiter=",")
fake4 = pd.read_csv(
    path_to_datasets+'/RihannaConcert2016En.txt', delimiter=",")
fake5 = pd.read_csv(path_to_datasets+'/swine-flu.txt', delimiter=";")
fake6 = pd.read_csv(path_to_datasets+'/UEFA_Euro_2016_En.txt', delimiter=",")

# Give labels to data before combining
fake1['fake'] = 1
fake2['fake'] = 1
fake3['fake'] = 1
fake4['fake'] = 1
fake5['fake'] = 1
fake6['fake'] = 1


def text_cleaning(text):
    document = text.split()
    for i in document:
        if 'RT' or 'https' or 'http' or '...' in i:
            document.remove(i)
    document = ' '.join(document)

    # Remove all the special characters
    document = re.sub(r'\W', ' ', text)

    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Converting to Lowercase
    document = document.lower()

    return document


fake1['content'] = fake1['content'].apply(text_cleaning)
fake2['content'] = fake2['content'].apply(text_cleaning)
fake3['content'] = fake3['content'].apply(text_cleaning)
fake4['content'] = fake4['content'].apply(text_cleaning)
fake5['content'] = fake5['content'].apply(text_cleaning)
fake6['content'] = fake6['content'].apply(text_cleaning)
# matrix1['content'] = matrix1['content'].apply(text_cleaning)
# matrix2['content'] = matrix2['content'].apply(text_cleaning)

# train/test split the text data and labels
# combining the two datasets

features = pd.concat([fake1['content'], fake2['content'], fake3['content'],
                      fake4['content'], fake5['content'], fake6['content']], axis=0)
# matrix1["content"], matrix2["content"]

labels = pd.concat([fake1['fake'], fake2['fake'], fake3['fake'],
                    fake4['fake'], fake5['fake'], fake6['fake']], axis=0)

# matrix1["isRumor"], matrix2["isRumor"]

# We seperate our train and test arrays

X_train, X_test, y_train, y_test = train_test_split(
    features, labels, random_state=42, shuffle=True)

# # not removing stop words to maintain word context

# Limitating the lenght of text and sequences
max_words = 100
max_len = 400

# Tokenization of text

token = Tokenizer(num_words=max_words, lower=True, split=' ')
token.fit_on_texts(X_train.values)
sequences = token.texts_to_sequences(X_train.values)
train_sequences_padded = pad_sequences(sequences, maxlen=max_len)

# Dimensioning of our arrays

embed_dim = 20

# Number of neurons of ur lstm

lstm_out = 64

batch_size = 32

# Definition of our network
model = Sequential()
model.add(Embedding(max_words, embed_dim, input_length=max_len))

# Using LSTM network
model.add(LSTM(lstm_out))

model.add(Dense(256))
model.add(Activation('relu'))  # To break the linearity of the network
model.add(Dropout(0.5))
model.add(Dense(1, name='out_layer'))
model.add(Activation('sigmoid'))  # Same
model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])

print(model.summary())

history = model.fit(train_sequences_padded, y_train, batch_size=batch_size,
                    epochs=15, validation_split=0.2)

# Train the model !

# Accuracy and Loss

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.legend(['Training', 'Validation'])
plt.ylabel('Accuracy (%)')
plt.xlabel('Epochs')
plt.xticks([0, 1, 2, 3, 4])

plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.legend(['Training', 'Validation'])
plt.ylabel('Loss (%)')
plt.xlabel('Epochs')
plt.xticks([0, 1, 2, 3, 4])

plt.show()

# Saving our model and token to src/training_datasets
model.save(path_to_datasets)

with open(path_to_datasets+'/token_tool', 'wb') as pickefile:
    pickle.dump(token, pickefile)
