# Import the libraries
import pandas as pd

class Clean_Tweets:
    """
    Description:
    ------------
    This module helps to clean the data from Twitter.
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.
        """
        df = self.df
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        self.df = df
        return df

    def drop_duplicate(self, columnId:list)->pd.DataFrame:
        """
        Description:
        ------------
        drop duplicate rows
        Inputs:
        -------
        columnId: list of unique column that descibe a single tweet
        """
        df = self.df
        df.drop_duplicates(subset=columnId)
        self.df = df
        return df

    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        ----
        
        ----
        
        df = df[df['created_at'] >= '2020-12-31' ]
        self.df = df
        return df
    
    def convert_to_numbers(self)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df = self.df
        df['polarity'] = pd.to_numeric(df['polarity'])
        df['subjectivity'] = pd.to_numeric(df['subjectivity'])
        df['retweet_count'] = pd.to_numeric(df['retweet_count'])
        df['favorite_count'] = pd.to_numeric(df['favorite_count'])
        self.df = df
        return df
    
    def remove_non_english_tweets(self)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        df = self.df
        df.drop(df[df.lang != 'en'].index,inplace=True)
        self.df = df
        
        return df