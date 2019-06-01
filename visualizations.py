#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:45:25 2019

@author: georgepatrick
"""
import sqlite3 #load all the nessecary staff again!
import pandas as pd
from pandas import DataFrame
from pandas import Series
import matplotlib.pyplot as plt


conn = sqlite3.connect('directors.db') #connect to the database, Please place the correct path
c = conn.cursor()



# A dataframe which contains all the data 
df = pd.read_sql_query('''SELECT * FROM directors''',conn) 

# 3 dataframes created with sql with the data of each director
df_hitch = pd.read_sql_query(''' SELECT * FROM directors WHERE keyword = 'Alfred Hitchcock' ''', conn)
df_scors = pd.read_sql_query(''' SELECT * FROM directors WHERE keyword = 'Martin Scorsese' ''', conn)
df_spiel = pd.read_sql_query(''' SELECT * FROM directors WHERE keyword = 'Steven Spielberg' ''', conn)

# Adding an attribute day to the previous 3 dataframes. This attribute will be used for the Time Series
df_hitch['day'] = pd.DatetimeIndex(df_hitch['date']).day
df_scors['day'] = pd.DatetimeIndex(df_scors['date']).day
df_spiel['day'] = pd.DatetimeIndex(df_spiel['date']).day

# A dataframe with the positve tweets for all directors
df_positive = pd.read_sql_query(''' SELECT * FROM directors WHERE sentiment = 'positive' ''', conn)



#### THE PLOT SHOW ####

# Sentiment of tweets in numbers by Director
positive_tweets = df["keyword"][df["sentiment"] == "positive"]
neutral_tweets = df["keyword"][df["sentiment"] == "neutral"]
negative_tweets = df["keyword"][df["sentiment"] == "negative"]
plt.hist([
        positive_tweets,  
        neutral_tweets, 
        negative_tweets], 
    stacked=True, label=["positive", "neutral", "negative"])
plt.legend()
plt.title("Sentiment for each Director") 
plt.xlabel("Directors") 
plt.ylabel("Number of tweets") #it's up to 500 since we extracted only 500 for each Director
plt.show()


# The average polarity for each director 
df.groupby("keyword")['polarity'].mean().plot(kind='bar') 
plt.title("Polarity mean by Director") 
plt.show()

#scatterplot for Hitchcock 
df_hitch.plot.scatter(x = 'number_of_words', y = 'followers',  c=df_hitch.polarity, alpha=0.3, colormap='bwr')
plt.xlim(-1,50)
plt.ylim(-50,15000)
plt.title("Hitchock's polarity-number of words-followers") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of followers")
plt.show()

#scatterplot for Scorsese 
df_scors.plot.scatter(x = 'number_of_words', y = 'followers',  c=df_scors.polarity, alpha=0.3, colormap='bwr')
plt.xlim(-1,50)
plt.ylim(-50,15000)
plt.title("Scorsese's polarity-number of words-followers") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of followers")
plt.show()

#scatterplot for Spielberg
df_spiel.plot.scatter(x = 'number_of_words', y = 'followers',  c=df_spiel.polarity, alpha=0.3, colormap='bwr')
plt.xlim(-1,50)
plt.ylim(-50,15000)
plt.title("Spielberg's polarity-number of words-followers") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of followers")
plt.show()

#General scatterplot for polarity-number of words-followers
df.plot.scatter(x = 'number_of_words', y = 'followers',  c=df.polarity, alpha=0.3, colormap='bwr')
plt.xlim(-1,50)
plt.ylim(-50,15000)
plt.title("Polarity and Number of Words for all tweets") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of followers")
plt.show()

#getting ready for the time series by creating new dataframes grouping the data by the day. 
series_hitch = df_hitch.groupby('day')['polarity'].mean()
series_scors = df_scors.groupby('day')['polarity'].mean()
series_spiel = df_spiel.groupby('day')['polarity'].mean()

#the time series of all directors from 10-01-2019 until 19-01-2019
plt.plot(series_hitch, label = 'Hitchcock')
plt.plot(series_scors, label = 'Scorsese')
plt.plot(series_spiel, label = 'Spielberg')
plt.axis([10, 19, 0, 0.03])
plt.ylim(-0.2,0.5)
plt.title("Time Series of Directors' Polarity ") 
plt.xlabel("Days of January 2019") 
plt.ylabel("Mean Polarity")
plt.legend()
plt.show()


#General scatterplot for polarity-number of words-followers-lollowers and retweets, the size of the dot indicates the number of followers
df.plot.scatter(x = 'number_of_words', y = 'retweets',  c=df.polarity, s=df.followers/4000,  alpha=0.3, colormap='cool')
plt.xlim(-1,50)
plt.ylim(-10,300)
plt.title("Polarity-Number of words-Retweets-Followers for all tweets") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of retweets")
plt.show()

#General scatterplot for polarity-number of words-retweets
df.plot.scatter(x = 'number_of_words', y = 'retweets',  c=df.polarity, alpha=0.3, colormap='coolwarm')
plt.xlim(-1,50)
plt.ylim(-10,300)
plt.title("Polarity-Number of words-Retweets for all tweets") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of retweets")
plt.show()

#positive tweets scatterplot
df_positive.plot.scatter(x = 'number_of_words', y = 'retweets',  c=df_positive.polarity, alpha=0.3, colormap='summer')
plt.xlim(-1,45)
plt.ylim(-10,500)
plt.title("Positve tweets Polarity") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of retweets")
plt.show()


#Hitchcock's polarity, number of words, retweets, followers
df_hitch.plot.scatter(x = 'number_of_words', y = 'retweets', s=df_hitch.followers/3000,  c=df_hitch.polarity, alpha=0.3, colormap='cool')
plt.xlim(-1,50)
plt.ylim(-10,500)
plt.title("Hitchock's Polarity-Number of words-Retweets-Followers") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of retweets")
plt.show()

#Hitchcock's polarity, number of words, retweets,
df_hitch.plot.scatter(x = 'number_of_words', y = 'retweets',c=df_hitch.polarity, alpha=0.3, colormap='cool')
plt.xlim(-1,50)
plt.ylim(-10,500)
plt.title("Hitchock's Polarity-Number of words-Retweets") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of retweets")
plt.show()

#scorsese's polarity, number of words, retweets
df_scors.plot.scatter(x = 'number_of_words', y = 'retweets',c=df_scors.polarity, alpha=0.3, colormap='BrBG')
plt.xlim(-1,40)
plt.ylim(-10,300)
plt.title("Scorsese's Polarity-Number of words-Retweets") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of retweets")
plt.show()

#spielberg's polarity, number of words, retweets
df_spiel.plot.scatter(x = 'number_of_words', y = 'retweets',c=df_spiel.polarity, alpha=0.3, colormap='BrBG')
plt.xlim(-1,50)
plt.ylim(-10,500)
plt.title("Spielberg's Polarity-Number of words-Retweets") 
plt.xlabel("Number of words in a tweet") 
plt.ylabel("Number of retweets")
plt.show()
