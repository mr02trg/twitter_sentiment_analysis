    
import tweepy
from textblob import TextBlob
import csv

# constants
NUM_SAMPLES = 3000
PAGE_SIZE = 100
SEARCH_STRING = 'trump'

TWEET = 0
POLARITY = 1
SUBJECTIVITY = 2

# numOfRecords = number of records to analyse, default: 1000
def get_tweets(api, samples=1000):
    
    pages = samples/PAGE_SIZE
    tweets = []

    curr_recs = api.search(SEARCH_STRING, lang='en', result_type='recent', count=PAGE_SIZE)
    curr_maxid = max(curr_recs, key=lambda x : x.id).id - 1
    tweets += curr_recs

    while(pages > 1):
        curr_recs = api.search(SEARCH_STRING, lang='en', result_type='recent', count=PAGE_SIZE, max_id=curr_maxid)
        curr_maxid = max(curr_recs, key=lambda x : x.id).id - 1
        tweets += curr_recs
        pages = pages - 1

    return tweets

def generate_data(tweets):
    data = []
    for tweet in tweets:
        dataRow = []

        # sentiment analysis using TextBlob
        analysis = TextBlob(tweet.text)    
           
        dataRow = [tweet.text, analysis.sentiment[0], analysis.sentiment[1]]
        data.append(dataRow)

    return data

def calculate_overall_sentiment(data):
    total_samples = 0
    total_polarity = 0
    positive = 0
    neutral = 0
    negative = 0
    for item in data:
        # only take into consideration of tweets that has some subjectivity (i.e. not purely objective)
        if (item[SUBJECTIVITY] > 0):
            if (item[POLARITY] > 0.5):
                positive += 1
            elif (item[POLARITY < -0.5]):
                negative += 1
            else:
                neutral += 1

            total_polarity += item[POLARITY]
            total_samples += 1

    
    avg_polarity = total_polarity / total_samples
    print('positive: ', positive)
    print('neutral: ', neutral)
    print('negative: ', negative)

    print('average polarity: ', avg_polarity)

def export_data(data):
    f = open("analysis.csv", "w", encoding='utf-8')

    writer = csv.writer(f)
    for item in data:
        writer.writerow(item)
    f.close()

# set up twitter api
consumer_key= 'YOUR_CONSUMER_KEY'
consumer_secret= 'YOUR_CONSUMER_SECRET'
access_token='YOUR_ACCESS_KEY'
access_token_secret='YOUR_CONSUMER_SECRET'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# get tweets
tweets = get_tweets(api)

# generate sentiment analysis data per tweet
data = generate_data(tweets)

# calculate overall sentiment polarity
avg_polarity = calculate_overall_sentiment(data)

# export analysis to csv
export_data(data)





