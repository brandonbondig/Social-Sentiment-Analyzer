import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
from statistics import mean
import pandas as pd
from config import *

# Inputs
UorS = input("Search by user(U) or search term(S): ").upper()
if UorS == "S":
    keyword = input('Search Term: ')
if UorS == "U":
    user_keyword = input("UserID: ")
sample_size = input('Sample size: ')
# sys.stdout = open('test.txt', 'w')
# Lists
tweets = []
times = []
neg = []
neu = []
pos = []
com = []

neg_avg = []
neu_avg = []
pos_avg = []
com_avg = []

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, secret_token)
api = tweepy.API(auth)

# Search by user
try:
    if UorS == "U":
        courser_user = tweepy.Cursor(api.user_timeline, id=user_keyword, tweet_mode='elevated').items(int(sample_size))

    # Search by tweets
    if UorS == "S":
        courser_search = tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode='elevated').items(int(sample_size))
except Exception as e:
    print(e)
    quit()
# Appends tweets to texts
try:
    if UorS == "U":
        for i in courser_user:
            tweets.append(i.text)
    if UorS == "S":
        for i in courser_search:
            tweets.append(i.text)
            times.append(i.created_at.strftime("%d-%m-%Y %H:%M:%S"))
except Exception as e:
    print(e)
    quit()
# Sentiment analyzer for individual accounts
analyzer = SentimentIntensityAnalyzer()

# Loop for fetching tweets in directories
for x in tweets:
    ss = analyzer.polarity_scores(x)

    # Appends data to lists
    neg.append(ss['neg'])
    neu.append(ss['neu'])
    pos.append(ss['pos'])
    com.append(ss['compound'])

    # Excludes fully neutral data
    if str(ss['neu']) != "1.0":
        neg_avg.append(ss['neg'])
        neu_avg.append(ss['neu'])
        pos_avg.append(ss['pos'])
        com_avg.append(ss['compound'])

try:
    # Average function
    def average(lst):
        return round(mean(lst), 2)

    # Tweets
    print('')
    print("--- Tweets ---")
    print(pd.DataFrame({"Tweets:": tweets,"Time:":times}))

    # DataFrame of sentiment
    print('')
    print('--- Social Sentiment Data ---')
    print('')
    df = pd.DataFrame({"Negative:": neg, "Neutral:": neu, "Positive:": pos, "Compound:": com})
    print(df)

    # Prints averages
    print('')
    print("--- Averages ---")
    print('')
    # Include neutral tweets
    print("- Neutral tweets included")
    print("Negative:", average(neg), "Neutral:", average(neu), "Positive:", average(pos), "Compound:", average(com))
    print('')
    # Exclude neutral tweets
    print("- Neutral tweets excluded")
    print("Negative:", average(neg_avg), "Neutral:", average(neu_avg), "Positive:", average(pos_avg), "Compound:", average(com_avg))

except Exception as e:
    print('')
    print("--- ERROR ---")
    print(e)
    quit()

sys.stdout.close()
