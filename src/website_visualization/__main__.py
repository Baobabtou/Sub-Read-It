import sys
sys.path.insert(1, '../src/')

from flask import Flask
from flask import render_template
from flask import send_from_directory
import json

import data_analysis.statistical_analysis
from data_analysis import semantics_analysis
import data_analysis.__init__
import wordcloud_visualization
from inspect import getsourcefile
from os.path import abspath
import os
import time

# Small utility to get the absolute path to the current module.
path_to_ressources = abspath(getsourcefile(lambda: 0))
path_to_ressources = os.path.join(path_to_ressources, '../imgs')
path_to_ressources = os.path.normpath(path_to_ressources)

app = Flask(__name__)

@app.route('/imgs/<path:path>')
def send_img(path):
	return send_from_directory('imgs', path)

@app.route('/')
def main_route():
	return render_template('index.html')
@app.route('/q/<subreddit>')
def get_data(subreddit):
	# Let's mesure the total time needed to analyse a subreddit.
	start_time = time.time()

	posts_to_analyse = 5 # Bigger = analysis is more accurate but slower.

	url = "https://www.reddit.com/r/" + subreddit + "/"
	print("Performing basic analysis ...")
	(stats_subreddit,posts,all_comments) = data_analysis.statistical_analysis.complete_analysis(url,posts_to_analyse)

	"""
		We need to provide an object with the following fields:
		- subjectivity
		- fake
		- popularity
		- polarity
		These fields need to be integers between 0 and 2 where 0 is the most positive and 2 is the most negative. 
	"""
	print("Generating wordcloud...")
	wordcloud_visualization.word_cloud(posts,all_comments,50,os.path.join(path_to_ressources,"img.png"))

	result = {}

	subreddit_text = data_analysis.statistical_analysis.convert_posts_to_text(posts,all_comments)

	polarity = stats_subreddit["average_polarity"] # between -1 and 1.
	subjectivity = stats_subreddit["average_subjectivity"] # between 0 and 1.
	comment_count = stats_subreddit["total_comment_count"]
	crossposts = stats_subreddit["average_crossposts"]
	debat = stats_subreddit["average_downvote_count"]/stats_subreddit["average_upvote_count"]

	print("Estimating fiability ...")
	fiability = data_analysis.__init__.sub_fiability_sklearn(posts,all_comments)

	# Fetch some more data.
	theme_data = semantics_analysis.analyze_theme(subreddit_text)
	theme_data_names = semantics_analysis.select_main(theme_data['proper_names'])
	theme_data_categ = semantics_analysis.select_main(theme_data['categories'])
	emotion_data = semantics_analysis.select_main(semantics_analysis.analyze_emotions(subreddit_text))
	emotion_strength = semantics_analysis.emotion_strength(subreddit_text)


	# create word cloud and save it 

	print("For r/"+subreddit,":")
	# Creating range of polarity and subjectivity to tell if a subreddit is neutral, positive or negative and subjective or objective

	print("Polarity = ",polarity)
	print("Subjectivity = ",subjectivity)
	print("CCount = ",comment_count)
	print("FakeNewsRisk = ",fiability)
	#creating range of polarity and subjectivity to tell if a subreddit is neutral, positive or negative and subjective or objective
	if -1 <= polarity < -.02:
		result["polarity"] = 2
	elif .02 <= polarity < 1:
		result["polarity"] = 0
	else:
		result["polarity"] = 1

	if 0 < subjectivity < .2:
		result["subjectivity"] = 0
	elif .2 <= subjectivity < .4:
		result["subjectivity"] = 1
	else:
		result["subjectivity"] = 2

	if 0 <= comment_count <= 100:
		result["popularity"] = 2
	elif 100 < comment_count <= 1000:
		result["popularity"] = 1
	else:
		result["popularity"] = 0

	if 0<=fiability<0.40:
		result["fake"] = 0
	elif 0.40<=fiability<=0.60:
		result["fake"]=1
	else:
		result["fake"]=2

	if 0<=emotion_strength<10:
		result["emotion_strength"]="Peu"
	elif 10<=emotion_strength<20:
		result["emotion_strength"]="Moyennement"
	else:
		result["emotion_strength"]="Beaucoup"

	if 0<=debat<0.25:
		result["up_down"]="Peu"
	elif 0.25<=debat<0.54:
		result["up_down"]="Moyennement"
	else:
		result["up_down"]="Beaucoup"

	result["emotions"] = emotion_data
	result["names"] = theme_data_names
	result["categories"] = theme_data_categ
	result["crossposts"] = crossposts

	end_time = time.time()	

	print("Time needed for analysis: ",(end_time - start_time)," seconds")

	return json.dumps(result)

app.run(debug=False,host='0.0.0.0', port=80)