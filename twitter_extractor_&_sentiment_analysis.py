#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:47:20 2019

@author: georgepatrick
"""

# Please provide your twitter credentials in the following variables;
## Also provide the your search term in the "query" variable;
### Then run the whole script
#### A new database will be created with the name 'keyword' which will contain a table with 50 tweets from 

#the credentials: api key, api secret, access token, access secret respectively;
ckey = 'ΧΧΧΧΧΧΧ'
csecret = 'ΧΧΧΧΧΧΧ'
atoken = 'ΧΧΧΧΧΧΧ'
asecret = 'ΧΧΧΧΧΧΧ'

query = 'Quentin Tarantino' #place inside the quotes your keyword 
until_date = '2019-01-20' # give the desirable date in this form 'YYYY-MM-DD' inside the quotes; FYI, tweets from the previous day will be extracted 
number_of_tweets = 100 # give the desirable number of tweets 


import sqlite3 #import all the necessary staff
import re
import json
import tweepy
import time
import datetime
from textblob import TextBlob 
import pandas as pd

conn = sqlite3.connect('keyword.db') # connect while creating a new database if it doesn’t exist 
c = conn.cursor()

c.execute('''CREATE TABLE keyword_table 
             (keyword, username, followers, tweets, retweets, text, date TEXT,
              location, hashtags, sentiment, polarity, number_of_words)''') # create a new table 

auth = tweepy.OAuthHandler(ckey, csecret) # setting up the connection with Twitter API
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# thetwitterextractor 
for tweet in tweepy.Cursor(api.search, q=query, tweet_mode = 'extended', lang="en", until= until_date).items(number_of_tweets): 
                                
    # for every tweet do the following...
    ## getting the data from a tweet and storing them to variables                
    keyword = query # a column keyword which will help distinguish the category of the tweets 
    username = (tweet.user.screen_name) 
    followers = (tweet.user.followers_count)
    tweets = (tweet.user.statuses_count)
    retweets = (tweet.retweet_count)
    text = (tweet.full_text) # extract the full text of the tweet; this does't happen for the retweets, SEE 'Discusion-Findings' at the report
    num_of_words = len(text.split()) # count the number of words in the text 
    date = (tweet.created_at)
    location = (tweet.user.location)  # if location in not provided we get an empty string, we will deal with that after the for loop
    hashtags = re.findall(r"#(\w+)", (tweet.full_text)) # extract the hashtags to a list from the text because it's easier!
    hashtags =', '.join(hashtags) # transform list to a strign, if hashtags are not provided, all we get is an empty string, we will deal with that after the for loop
                                
    cleaned_text = ' '.join(re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)'," ", text).split()) #clean text using re
                            
    analysis = TextBlob(cleaned_text)  # sentiment analysis takes place here using textblob
    tweet_polarity = analysis.sentiment.polarity    
    if tweet_polarity > 0:                 
        sentiment = 'positive'
    elif tweet_polarity == 0:
        sentiment = 'neutral'                  
    else:
        sentiment = 'negative'     
                                
                                
                            
    # Insert a row of data in the corresponing table
    c.execute('''INSERT INTO keyword_table VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', 
            (keyword, username, followers, tweets, retweets, text, date, 
             location, hashtags, sentiment, tweet_polarity, num_of_words))
    conn.commit() # commit every time a new tweet loads to the table                   


#dealing with empty strings the table, specifically with the location and hashtags attributes.  
c.execute('''UPDATE keyword_table set location = null where location = '' ''')
c.execute('''UPDATE keyword_table set hashtags = null where hashtags = '' ''')

##Despite that we set the empty strigns as NULL, viewing the database with a DB browser shows this values as an empty box.

#see the results as dataframe
df = pd.read_sql_query('''SELECT * FROM keyword_table''',conn)
print (df)

