#!/usr/bin/python
import tweepy  

class TweetReader:
   def __init__(self):
      consumer_key = ''  
      consumer_secret = ''  
      access_token = ''  
      access_token_secret = '' 
      auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
      self.api = tweepy.API(auth) 

   def get_tweets(self):
      tweets = self.api.mentions_timeline()
      return tweets