"""
We use the PassiveAgressiveClassifier from Sklearn, we can change that afterwards
Need to pip install : pandas, sklearn, pickle (numpy and matplotlib of course)
"""
import numpy as np
import pandas as pd
import os.path
from inspect import getsourcefile
from os.path import abspath

import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt


path_to_datasets = abspath(getsourcefile(lambda:0))
path_to_datasets = os.path.join(path_to_datasets,'../../../trained_models')
path_to_datasets = os.path.normpath(path_to_datasets)


# Given the diversity of different datasources for training available online, we need a common format for analyse them.
# We use the following format as a common ground:
# A dataframe which has the columns 'text : str' and 'label : 0,1', 0 for TRUE and 1 for FAKE

def train_model(data, model_stored="trained_models/model.sav", vector_stored="trained_models/vectorizer.sav"):
	"""
	Function that initializes/upgrades (if the file model_stored already exists of not) our pac model on a given dataset 
	and returns the result of the training
	plus saves the new model in store_in
	NB : data must be a dataframe with 'text' and 'label'
	"""

	# The pac model is initialized or retrieved 
	if os.path.exists(model_stored):
		pac = pickle.load(open(model_stored, 'rb'))
		# We delete the content of the file to store the updated version later
		open(model_stored, 'w').close()
	else:
		pac = PassiveAggressiveClassifier(max_iter=1000)

	# The vectorizer is initialized or retrieved
	if os.path.exists(vector_stored):
		tfidf_vectorizer = pickle.load(open(vector_stored, 'rb'))
		open(vector_stored, 'w').close()
	else:
		tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
	
	# one can modifiy the test_size, or the random_state : the data is split for training/testing randomly
	x_train, x_test, y_train, y_test = train_test_split(
		data['text'], data['label'], test_size=0.3, random_state=7, shuffle = True)

	# applied on the 2 sets of text, firstly we have to fit the vectorizer
	tfidf_train = tfidf_vectorizer.fit_transform(x_train.values.astype('U'))
	tfidf_test = tfidf_vectorizer.transform(x_test.astype('U'))
	
	# the model learns with the x_train data:
	pac.fit(tfidf_train, y_train)

	# testing with x_test :
	y_pred = pac.predict(tfidf_test)
	
	# displaying accuracy and confusion_matrix (optional)
	score = accuracy_score(y_test, y_pred)
	print(f'Accuracy: {round(score*100,2)}%')
	print(confusion_matrix(y_test, y_pred, labels=None))

	#we store the updated model for further training, and the vectorizer too
	pickle.dump(pac, open(model_stored, 'wb'))
	pickle.dump(tfidf_vectorizer, open(vector_stored, "wb"))


def evaluate(data_text, model_stored="model.sav", vector_stored = "vectorizer.sav"):
	"""
	Takes a column-dataframe of ["text"], and return an array of same dimension with 0(Real), 1(Fake) for each text
	"""
	# We load the model
	model_stored = os.path.join(path_to_datasets,model_stored)
	vector_stored = os.path.join(path_to_datasets,vector_stored)

	pac = pickle.load(open(model_stored, 'rb'))
	# We load the appropriate Vectorizer
	tfidf_vectorizer = pickle.load(open(vector_stored, 'rb'))
	# We transform the data to analyze
	tfidf_test = tfidf_vectorizer.transform(data_text.astype('U'))
	# Which now can be analysed by the loaded model
	evaluation = pac.predict(tfidf_test)
	return evaluation

if __name__=="__main__":
	# Initializing the model, not necessary if there's already one saved
	# You can upgrade an already existing model by changing df
	# For the demo, we charge the train.csv file from Kaggle.com, which already has columns 'text' and 'label' :
	df = pd.read_csv("training_datasets/train.csv")
	train_model(data = df) 
	# Testing our model on the Fake dataset --> only 1 expected ...
	data = pd.read_csv("training_datasets/Fake.csv")
	data_text = data['text']
	y = evaluate(data_text)
	print(y)
	print(np.sum(y)/len(data_text))


