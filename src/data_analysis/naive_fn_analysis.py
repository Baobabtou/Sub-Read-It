import sys
sys.path.insert(1, './src/')
from nltk.corpus import stopwords
import textblob as tb
import data_collect as dc
import statistical_analysis as sub
import semantics_analysis as sa


def sent_com(com):
    '''Returns as a list the sum of the polarities and subjectivities of the answers of a comment (the comment itself is not taken into account!)'''
    s = 0
    t = 0
    if len(com['comments']) != 0:
        for comment in com['comments']:
            res = sent_com(comment)
            blobAnalysis = tb.TextBlob(comment['text'])
            if blobAnalysis.sentiment.subjectivity!=0:#taking into account only the comments which subjectivty isn't zero
                s += res[0] + blobAnalysis.sentiment[1]
                t += res[1] + 1
    return[s, t]

def subj_subreddit(posts,max_post = 5):
    '''Returns the avg polarity and subjectivity of a subreddit/dataframe'''
    s = 0
    tot = 0
    # print(len(posts),"posts collected")
    for i in range(min(len(posts),max_post)):
        # print(i+1,"/",len(posts.index),"posts collected for the subreddit ") # Nice debug because the method takes time.
        tot += 1
        title = tb.TextBlob(posts['title'][i])
        s += title.sentiment.subjectivity
        if posts['num_comments'][i] != 0:
            comments = dc.collect_comments(posts['permalink'][i])
            for comment in comments:
                res = sent_com(comment)
                t = tb.TextBlob(comment['text'])
                s += (res[0] + t.sentiment.subjectivity) # taking into acount subjectivity of the first comments of the tree
                tot += res[1]
        tot += posts['num_comments'][i] # adding first comment generation
    return s/tot

def fake_naif(subreddit):
    url = "https://www.reddit.com/r/" + subreddit + "/"
    posts=dc.collect_posts(url)
    upvote_tot=0
    for i in range (0,len(posts)):
        upvote_tot+=posts['upvote_ratio'][i]
    upvote_moy=upvote_tot/len(posts)
    subj_moy=subj_subreddit(posts,25)
    downvote_moy=1-upvote_moy
    fake_rate=(subj_moy+downvote_moy)/2 #more subjectivty => more fake, more downvote_ratio => more fake
    if 0<fake_rate<0.3:
        print(fake_rate,':This subreddit is fairly reliable')
    elif 0.3<=fake_rate<0.5:
        print(fake_rate,':This subreddit is quite reliable but contains some misinformation ')
    elif 0.5<=fake_rate<0.7:
        print(fake_rate, ':This subreddit is not really reliable ')
    else:
        print(fake_rate, ":That's fake news !!")

if __name__ == '__main__':
    fake_naif('conspiracy')