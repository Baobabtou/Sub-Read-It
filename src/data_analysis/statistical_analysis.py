"""
Perform all analysis that do not require any database / model:
	- Retreiving the number of likes / dislikes
	- Retreive the number of times data was been shared.
	- Retreive the comments for all posts of a subreddit
	- etc ...
"""

import sys
sys.path.insert(1, './src/')
from nltk.corpus import stopwords
import textblob as tb
import data_collect as dc




def stat_com(com):
	"""
		Returns as a list the number of ups, downs and the number of comments in answer to a comment (the comment itself is not taken into account)
	"""
	ups = 0
	downs = 0
	tot = 0
	if len(com['comments']) != 0:
		for comment in com['comments']:
			stats = stat_com(comment)
			ups += (stats[0] + comment['ups'])
			downs += (stats[1] + comment['downs'])
			tot += (stats[2] + 1)
	return [ups, downs, tot]


def stat_subreddit(posts,all_comments,max_post = 5):
	"""
		Takes a dataframe and analyse the average number of upvotes and downvotes
		Returns as a list the average ups, ups-downs, downs and the number of comments of a subreddit/dataframe
	"""
	tot_ups = 0
	tot_downs = 0
	tot_com = 0
	for i in range(min(len(posts.index),len(all_comments))):
		tot_ups += posts['ups'][i]
		tot_downs += posts['downs'][i]
		tot_com += 1
		# the commentaries below the post
		if posts['num_comments'][i] != 0:
			comments = all_comments[i]
			for comment in comments:
				stats = stat_com(comment)
				# add root comment count
				tot_ups += (stats[0] + comment["ups"])#taking into acount 'ups' of the first comments of the tree
				tot_downs += (stats[1] + comment["downs"])#taking into acount 'downs of the first comments of the tree
				tot_com += stats[2]
		tot_com += posts['num_comments'][i]  # 1st generation comments
	return [tot_ups/tot_com, (tot_ups-tot_downs)/tot_com, tot_downs/tot_com, tot_com]


def sent_com(com):
	'''Returns as a list the sum of the polarities and subjectivities of the answers of a comment (the comment itself is not taken into account!)'''
	p = 0
	s = 0
	t = 0
	if len(com['comments']) != 0:
		for comment in com['comments']:
			res = sent_com(comment)
			blobAnalysis = tb.TextBlob(comment['text'])
			p += res[0] + blobAnalysis.sentiment[0]
			s += res[1] + blobAnalysis.sentiment[1]
			t += res[2] + 1
	return[p, s, t]


def sent_subreddit(posts,all_comments,max_post = 5):
	'''Returns the avg polarity and subjectivity of a subreddit/dataframe'''
	p = 0
	s = 0
	tot = 0
	for i in range(min(len(posts),len(all_comments))):
		tot += 1
		title = tb.TextBlob(posts['title'][i])
		p += title.sentiment.polarity
		s += title.sentiment.subjectivity
		if posts['num_comments'][i] != 0:
			comments = all_comments[i]
			for comment in comments:
				res = sent_com(comment)
				t = tb.TextBlob(comment['text'])
				p += (res[0] + t.sentiment.polarity)#taking into acount polarity of the first comments of the tree
				s += (res[1] + t.sentiment.subjectivity)#taking into acount subjectivity of the first comments of the tree
				tot += res[2]
		tot += posts['num_comments'][i]#adding first comment generation
	return [p/tot, s/tot]

#other relevant analyses, to complete if needed:
def further_subreddit(posts):
	#avg crossposts
	total_len = len(posts.index)
	total_crossposts = sum([i for i in posts["num_crossposts"]])
	return total_crossposts/total_len

def convert_posts_to_text(posts,all_comments,max_data = 200):
	texts = []
	for i in range(min(len(posts.index),len(all_comments))):
		texts.append(posts['title'][i])
		if len(texts) > max_data:
			break
		# the comments below the post
		if posts['num_comments'][i] != 0:
			comments = all_comments[i]
			for j in range(len(comments)):
				 texts.append(comments[j]["text"])
	return ' '.join(texts)

def complete_analysis(url, max_posts = 15):
	#return all the data collected by the precedent functions
	posts = dc.collect_posts(url)

	# collect all comments
	all_comments = []
	for i in range(min(len(posts.index),max_posts)):
		if posts['num_comments'][i] != 0:
			comments = dc.collect_comments(posts['permalink'][i])
			all_comments.append(comments)
		else:
			all_comments.append([])

	# print(len(posts),"posts collected and ",len(all_comments)," top-level comments obtained in thoses posts")

	statistics = stat_subreddit(posts,all_comments)
	sentiments = sent_subreddit(posts,all_comments)
	other = further_subreddit(posts)
	return ({
		"average_polarity": sentiments[0],
		"average_subjectivity": sentiments[1],
		"total_comment_count": statistics[3],
		"average_upvote_count": statistics[0],
		"average_downvote_count": statistics[2],
		"average_crossposts": other
	},posts,all_comments)


if __name__ == '__main__':
	print(complete_analysis("https://www.reddit.com/r/nottheonion/"))
	pass
