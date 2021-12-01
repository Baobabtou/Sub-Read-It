"""
Code for wordcloud visualization.
Used to be able to do all kinds of matplotlib visualization.
Kept in a seperate directory for legacy purposes and if we need to add matplotlib specific visualization at some point.
"""
import sys
sys.path.insert(1, './src/')

# import matplotlib.pyplot as plt
import wordcloud as wc
import data_analysis.text_analysis as ta

def word_cloud(posts, all_comments, number_words, file_path= "result.png"):
	"""
	Creates a word cloud of the words used in the subreddit referenced by 'url'"""

	cloud = wc.WordCloud(background_color="white", max_words=1000)

	# generate word cloud
	cloud.generate_from_frequencies(ta.word_counts(posts,all_comments,number_words))

	# show
	cloud.to_file(file_path)
	# plt.imshow(cloud, interpolation="bilinear")
	# plt.axis("off")
	# plt.show()
	
if __name__=='__main__':
	posts = dc.collect_posts("https://www.reddit.com/r/politics/")
	all_comments = []
	for i in range(min(len(posts.index),max_posts)):
		if posts['num_comments'][i] != 0:
			comments = dc.collect_comments(posts['permalink'][i])
			all_comments.append(comments)
		else:
			all_comments.append([])
	
	word_cloud(posts,all_comments,50)