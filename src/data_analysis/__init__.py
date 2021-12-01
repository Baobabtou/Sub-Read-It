# -*- coding: utf-8 -*-
import sys
sys.path.insert(1, './src/')
sys.path.insert(1, './src/data_analysis')
import os
# Disable GPU use:
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # no gpu

using_tensorflow = False
import pickle

if using_tensorflow:
	from tensorflow.keras.preprocessing.sequence import pad_sequences
	from tensorflow import keras
from inspect import getsourcefile
from os.path import abspath
import sys
import data_collect as dc
from pandas import DataFrame
import textblob as tb
from data_analysis import pac_fn_analysis

# Small utility to get the absolute path to the current module.
path_to_datasets = abspath(getsourcefile(lambda:0))
path_to_datasets = os.path.join(path_to_datasets,'../../../training_datasets')
path_to_datasets = os.path.normpath(path_to_datasets)

if using_tensorflow:
	# Load model and token
	token = None
	model = keras.models.load_model(path_to_datasets)
	# token is useful to make string fit the structure of our model
	with open(path_to_datasets+'/token_tool', 'rb') as token_tool:
		token = pickle.load(token_tool)

def is_text_fake(text):
	if not using_tensorflow:
		print("Tensorflow is not loaded!")
		return 0
		# Tests if a string is fake news or not.
		# Returns 1 if it is, 0 if it isn't.
	seq = token.texts_to_sequences([text])
	padded = pad_sequences(seq, maxlen=400)  # value taken to train our network
	pred = model.predict(padded)
	return pred[0][0]


def sub_fiability_tensorflow(posts,all_comments):
	if not using_tensorflow:
		print("Tensorflow is not loaded!")
		return 0

	print('Analyzing subreddit fiability ...')
	ind_title = list(posts.keys()).index('title')
	ind_url = list(posts.keys()).index('permalink')
	fiabilities = []
	i = 0
	for post in posts.values:
		comments = []
		if i < len(all_comments):
			comments = all_comments[i]
		i += 1
		texts_post = post[ind_title]
		for comment in comments:
			text_comment = comment['text']
			if text_comment != '[removed]':
				texts_post+=text_comment+' '
		fiabilities.append(is_text_fake(texts_post))
	#print(fiabilities)
	if len(fiabilities)!=0:
		return(sum(fiabilities)/len(fiabilities))
	else:
		print("Aucun texte dans la subreddit")
		return 0

#début de la partie sklearn, tensorflow ci-dessus à supprimer ?
#takes a commentary and returns a list of text below this commentary (commentary not included)
def get_text_comment(com):
	text_comment = []
	if len(com['comments']) != 0:
		for comment in com['comments']:
			text_comment += (get_text_comment(comment) + [comment['text']])
	return text_comment

def sub_fiability_sklearn(posts,all_comments):
	ind_title = list(posts.keys()).index('title')
	ind_url = list(posts.keys()).index('permalink')
	texts = []
	i = 0

	for post in posts.values:
		comments = []
		if i < len(all_comments):
			comments = all_comments[i]
		i += 1
		texts_post = post[ind_title]
		texts.append(texts_post)
		for comment in comments:
			text_comment = get_text_comment(comment) + [comment['text']]
			for string in text_comment:
				if string == '[removed]':
					text_comment.remove(string)
			texts += text_comment
	if texts!=[]:
		texts = {'text':texts}
		texts = DataFrame(texts)['text']
		result = pac_fn_analysis.evaluate(texts)
		return sum(result)/len(result)
	else:
		print("Aucun texte dans la subreddit")
		return 0

"""true_data = pd.read_csv('training_datasets/train.csv')
fiabs = []
for text in true_data['text'][:150]:
	print(is_text_fake(text))"""
if __name__=='__main__':
	posts = dc.collect_posts('https://www.reddit.com/r/news/')
	all_comments = []
	for i in range(min(len(posts.index),max_posts)):
		if posts['num_comments'][i] != 0:
			comments = dc.collect_comments(posts['permalink'][i])
			all_comments.append(comments)
		else:
			all_comments.append([])
	print(sub_fiability_sklearn(posts,all_comments))