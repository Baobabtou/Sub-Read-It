"""
Performs TextBlob and vocab based analysis
"""

import sys
sys.path.insert(1, './src/')

import data_collect as dc
import textblob as tb
import pandas as pd
from nltk.corpus import stopwords
import wordcloud as wc
import matplotlib.pyplot as plt

def words_com(com):
	"""
		Returns as a list the words used in a comment and all its answers
	"""
	Stopwords = list(stopwords.words('english')) + ['https',"gt","lt",'amp','like','i','if','in','subreddit','please', 'the', 'much', 'it', 'that', 'get', 'well']
	L = tb.TextBlob(com['text']).words
	useful_words = [w for w in L if w.isalpha() and w.lower() not in Stopwords]
	if len(com['comments']) != 0:
		for comment in com['comments']:
			useful_words += words_com(comment)  
	return useful_words


def word_counts(posts, all_comments, number_of_words,max_post = 5):
	"""
	Returns the count of the words in a subreddit , not analysing the title of the posts
	"""
	words={}
	for i in range(min(len(posts),5)):
		if posts['num_comments'][i]!=0:
			comments = all_comments[i]
			for comment in comments:
				for word in words_com(comment): # checking if the word is already in the dictionnary 
					if word not in words:
						words[word] = 1
					else:
						words[word] += 1
	important_words = sorted(words.items(), key = lambda x: x[1], reverse = True)
	
	return dict(important_words[:number_of_words]) # returning only the 'number_of_words' most used words



if __name__=='__main__':
	posts = dc.collect_posts("https://www.reddit.com/r/politics/")
	all_comments = []
	for i in range(min(len(posts.index),max_posts)):
		if posts['num_comments'][i] != 0:
			comments = dc.collect_comments(posts['permalink'][i])
			all_comments.append(comments)
		else:
			all_comments.append([])

	print(word_counts(posts,all_comments, 100))

