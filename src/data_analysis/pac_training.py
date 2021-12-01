"""
This code is used to train the sklearn model.
All it does is fetch the data needed for training and calls the train method inside pac.
You can choose here on what data you want to train.
"""
import sys
sys.path.insert(1, './src/')
import data_collect as dc
import pandas as pd
from data_analysis import pac_fn_analysis
import pickle

def get_text_comment(com):
	text_comment = []
	if len(com['comments']) != 0:
		for comment in com['comments']:
			text_comment += (get_text_comment(comment) + [comment['text']])
	return text_comment

''' 
takes the url of a subreddit which veracity us known, and returns a dataframe that can be used for training
'''
def create_dataframe(url, veracity):
    posts = dc.collect_posts(url)
    ind_title = list(posts.keys()).index('title')
    ind_url = list(posts.keys()).index('permalink')
    texts = []
    for post in posts.values:
        comments = dc.collect_comments(post[ind_url])
        texts_post = post[ind_title]
        texts.append(texts_post)
        for comment in comments: 
            text_comment = get_text_comment(comment) + [comment['text']]
            for string in text_comment:
                if string == '[removed]': 
                    text_comment.remove(string)
            texts += text_comment
    
    texts = {'text':texts}
    dataframe = pd.DataFrame.from_dict(texts)
    #add the 0, 1    
    if veracity:
        dataframe['label'] = 0
    else:
        dataframe['label'] = 1
    return dataframe


""" To train the current model (initialized in pac_fn_analysis.py) : example (it takes a lot of time) """
if __name__=="__main__":
    #FAKE DATAFRAMES    
    dataframe_fake_1 = create_dataframe('https://www.reddit.com/r/BirdsArentReal/', False) 
    dataframe_fake_2 = create_dataframe('https://www.reddit.com/r/conspiracy/', False)
    dataframe_fake_3 = create_dataframe('https://www.reddit.com/r/AmItheAsshole/', False)
    dataframe_fake_4 = create_dataframe('https://www.reddit.com/r/MemeThatNews/', False)
    #TRUE DATAFRAMES
    dataframe_true_1 = create_dataframe('https://www.reddit.com/r/askscience/', True)
    dataframe_true_2 = create_dataframe('https://www.reddit.com/r/technology/', True)
    dataframe_true_3 = create_dataframe('https://www.reddit.com/r/Ornithology/', True)
    dataframe_true_4 = create_dataframe('https://www.reddit.com/r/math/', True)

    #CONCATENATE
    dataframe = pd.concat([dataframe_fake_1, dataframe_true_1, dataframe_fake_2, dataframe_true_2,dataframe_fake_3, dataframe_true_3, dataframe_fake_4, dataframe_true_4])
    #saving the mega_dataset from Reddit
    dataframe.to_pickle("training_datasets/dataframe.pkl")

    # Using the dataset, takes less time if it is already charged
    df = pd.read_pickle("training_datasets/dataframe.pkl")
    # Training our model with the dataset
    pac_fn_analysis.train_model(df)


# To add more data in the training dataset, open df directly and concatenate with other dataframes calling create_dataframe
# See the example below for more details

# df = pd.read_pickle("training_datasets/dataframe.pkl")
# df_1 = create_dataframe('https://www.reddit.com/r/programming/', True)
# df_2 = create_dataframe('https://www.reddit.com/r/news/', True)
# df_3 = create_dataframe('https://www.reddit.com/r/gardening/', True)
# df_4 = create_dataframe("https://www.reddit.com/r/wallstreetbets/", False)
# df_5 = create_dataframe('https://www.reddit.com/r/reptilians/', False)


# data = pd.concat([df, df_1, df_2, df_4, df_5])
# data.to_pickle("training_datasets/dataframe_2.pkl")

# df = pd.read_pickle("training_datasets/dataframe_2.pkl")
# pac_fn_analysis.train_model(df)