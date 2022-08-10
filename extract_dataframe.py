import json
import pandas as pd
from textblob import TextBlob
import re


def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = [tweet["user"]["statuses_count"] for tweet in self.tweets_list]

        return statuses_count

        
    def find_full_text(self)->list:
        text = []
        for tweet in self.tweets_list:
            try:
                text.append(tweet["retweeted_status"]["full_text"])
            except KeyError:
                text.append(tweet["full_text"])

        return text

       
    
    def find_sentiments(self, text)->list:
        sentiment = [TextBlob(txt).sentiment for txt in text]
        subjectivity = [TextBlob(txt).sentiment.subjectivity for txt in text]
        polarity = [TextBlob(txt).sentiment.polarity for txt in text]
        
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at = [tweet["created_at"] for tweet in self.tweets_list]
       
        return created_at

    def find_source(self)->list:
        source = [tweet["source"] for tweet in self.tweets_list]

        return source

    def find_screen_name(self)->list:
        screen_name = [tweet["user"]["screen_name"] for tweet in self.tweets_list]
        return screen_name

    def find_followers_count(self)->list:
        followers_count = [tweet["user"]["followers_count"] for tweet in self.tweets_list]
        return followers_count

    def find_friends_count(self)->list:
        friends_count = [tweet["user"]["friends_count"] for tweet in self.tweets_list]
        return friends_count

    def is_sensitive(self)->list:
        is_sensitive = []
        for tweet in self.tweets_list:
            try:
                is_sensitive.append(tweet["possibly_sensitive"])
            except KeyError:
                is_sensitive.append('')
        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = []
        for tweet in self.tweets_list:
            try:
                favourite_count.append(tweet["retweeted_status"]["favorite_count"])
            except:
                favourite_count.append(0)
        return favourite_count
        
    
    def find_retweet_count(self)->list:
        retweet_count = []
        for tweet in self.tweets_list:
            try:
                retweet_count.append(tweet["retweeted_status"]["retweet_count"])
            except:
                retweet_count.append(0)
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = [tweet['entities']['hashtags'] for tweet in self.tweets_list]
        return hashtags

    def find_mentions(self)->list:
        mentions = [tweet["entities"]["user_mentions"] for tweet in self.tweets_list]
        return mentions


    def find_location(self)->list:
        location = []
        for tweet in self.tweets_list:
                try:
                    location.append(tweet["user"]["location"])
                except TypeError:
                    location = ''
        
        return location

    def find_lang(self)->list:
        lang = [tweet['lang'] for tweet in self.tweets_list]
        return lang

    def clear_text(self,text)->list:
        temp = [txt.lower() for txt in text]
        txt_clear = [re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", txt) for txt in temp]
        return txt_clear

    def get_sentiment(self,polarity):
        sentiment = []
        for pol in polarity:
            if pol < 0:
                sentiment.append("Negative")
            elif pol >0:
                sentiment.append("Positive")
            else:
                sentiment.append("Neutral")
        return sentiment
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at','source','original_text','clean_text','polarity','subjectivity','sentiment',\
            'lang','favorite_count','retweet_count','original_author','followers_count','friends_count',\
                'possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        clean_txt = self.clear_text(text)
        sentiment, polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, clean_txt, sentiment, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('data/processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text','sentiment','polarity','subjectivity','lang','favorite_count', 'retweet_count', 
    'original_author','followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
    _, tweet_list = read_json("data/global_twitter_data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(save=True) 

    # use all defined functions to generate a dataframe with the specified columns above