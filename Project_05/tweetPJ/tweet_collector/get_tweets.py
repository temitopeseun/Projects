import time
import tweepy
import os
import pymongo


client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.twitter


 
##################
# Authentication # 
###################
BEARER_TOKEN = "AAAAAAAAAAAAAAAAScNn0Q%3DWn8jwet06Bw3yYSxMGGCKS7fSCDRXxs6WNKSG"



##################
# make sure you run this codeline in terminal:///$ 'python get_tweets.py'
##################
 

##################
# Authentication #
##################



client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)

########################
# Get User Information #
########################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_user
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

response = client.get_user(
    username='elonmusk',
    user_fields=['created_at', 'description', 'location',
                 'public_metrics', 'profile_image_url']
)

user = response.data

print(dict(user))


#########################
# Get a user's timeline #
#########################

# https://docs.tweepy.org/en/stable/pagination.html#tweepy.Paginator
# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_tweets
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

cursor = tweepy.Paginator(
    method=client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics']
).flatten()

# ).flatten(limit=20)

for tweet in cursor:
    print(tweet.text)


#####################
# Search for Tweets #
#####################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_recent_tweets
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

# - means NOT
search_query = "elon musk -is:retweet -is:reply -is:quote lang:en -has:links"

cursor = tweepy.Paginator(
    method=client.search_recent_tweets,
    query=search_query,
    tweet_fields=['author_id', 'created_at', 'public_metrics'],
).flatten(limit=20)

for tweet in cursor:

    print(tweet.text+'\n')
    db.tweets.insert_one(dict(tweet))

