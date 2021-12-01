# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 23:22:33 2020

@author: lembe
"""
import sys
sys.path.insert(1, './src/')

import data_analysis
import pytest

# Collect some data to do the tests
posts = dc.collect_posts("https://www.reddit.com/r/politics/")
all_comments = []
for i in range(min(len(posts.index),max_posts)):
	if posts['num_comments'][i] != 0:
		comments = dc.collect_comments(posts['permalink'][i])
		all_comments.append(comments)
	else:
		all_comments.append([])

def test_machine_learning():
	""" we can apply our network to each string we want. And to be able to do so we must transform it into an object recognizable by our network
	and to achieve it we will use the variable token used in our network algorithm to structure dataset for training. So we will use it again
	so that we can appy our model to any kind of string"""
	word_counts(posts,all_comments, 100)
	pass