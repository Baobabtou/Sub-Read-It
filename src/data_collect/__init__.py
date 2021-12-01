"""
Code that retreives data from the reddit website.
All the "networking" code happens here.
"""
import requests
from lxml.html import fromstring
import json
import pandas as pd

headers = {
	'User-Agent': 'Reddit stats bot: Make stats about reddit posts for a learning project',
	'From': 'CentraleSupelec (Engineering school in France)'
}

def get_page_title(url):
	"""
		Returns the title of a webpage.
		Examples:
			get_page_title("https://stackoverflow.com/questions/26812470/how-to-get-page-title-in-requests") == "python - How to get page title in requests - Stack Overflow"
	"""
	r = requests.get(url)
	tree = fromstring(r.content)
	return tree.findtext('.//title')


def restructure_comments(raw_json):
	"""
		Recursive function that converts the json from the reddit api to a clean structure as described by the comment
		on collect_comments
	"""
	result = []
	for el in raw_json:
		if "author" in el["data"] and "body" in el["data"]:
			comment = {
				"author": el["data"]["author"],
				"text": el["data"]["body"],
				"ups": el["data"]["ups"],
				"downs": el["data"]["downs"],
			}
			if el["data"]["replies"] != "":
				comment["comments"] = restructure_comments(el["data"]["replies"]["data"]["children"])
			else:
				comment["comments"]=[]
			result.append(comment)
	return result

def collect_comments(post, url = None):
	"""
		Url example:
			https://reddit.com/r/PoliticalCompassMemes/comments/jv2xo8/checkmate_libleft/
		Posts example:
			r/PoliticalCompassMemes/comments/jv2xo8/checkmate_libleft/
		Fetches the comments of a reddit post.
		Returns a python list with the following structure :
		[
			{
				'text':'',
				'author':'',
				'ups':3, # likes
				'downs':1 # dislikes
				'comments': [ list of comments, same structure, it's a tree]
			}
		]

	"""
	if url!=None:
		api_url = url + "comments.json"
	else:
		api_url = "https://reddit.com" + post + "comments.json"
	r = requests.get(api_url, headers=headers)
	try:
		data = json.loads(r.text)
		data = data[1]["data"]["children"] # get the top level comments
		return restructure_comments(data)
	except:
		print("Unable to parse json response from server.")
		print(r.text)
		return []

def collect_posts(url, order="hot", infos_kept = ['title', 'permalink','ups','downs','upvote_ratio','created_utc','num_comments','author', 'num_crossposts']):
	"""
	Collects posts of the subreddit from given url (url example: https://www.reddit.com/r/nottheonion/)
	Returns a dataframe with the information chosen in info_kept list with the following structure
	"""

	api_url = url + order +".json"
	r = requests.get(api_url, headers=headers)
	data = json.loads(r.text)["data"]["children"]
	posts_data = dict(pd.DataFrame(data = data)['data']).values()
	panda_data = pd.DataFrame(data = posts_data)[infos_kept]
	return panda_data


if __name__ == '__main__':
	print(collect_comments(collect_posts("https://www.reddit.com/r/news/")['permalink'][4]))