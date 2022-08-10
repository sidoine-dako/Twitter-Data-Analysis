import unittest
import pandas as pd
import sys,os

sys.path.append(os.path.abspath(os.path.join('..')))

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor

# For unit testing the data reading and processing codes, 
# we will need about 5 tweet samples. 
# Create a sample not more than 10 tweets and place it in a json file.
# Provide the path to the samples tweets file you created below
sampletweetsjsonfile = "tests/sampletweets.json"   #put here the path to where you placed the file e.g. ./sampletweets.json. 
_, tweet_list = read_json(sampletweetsjsonfile)

columns = [
    "created_at",
    "source",
    "original_text",
    "clean_text",
    "polarity",
    "subjectivity",
    "sentiment",
    "lang",
    "favorite_count",
    "retweet_count",
    "original_author",
    "screen_count",
    "followers_count",
    "friends_count",
    "possibly_sensitive",
    "hashtags",
    "user_mentions",
    "place",
    "place_coord_boundaries",
]


class TestTweetDfExtractor(unittest.TestCase):
    """
		A class for unit-testing function in the fix_clean_tweets_dataframe.py file

		Args:
        -----
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""

    def setUp(self) -> pd.DataFrame:
        self.df = TweetDfExtractor(tweet_list[:5])
        # tweet_df = self.df.get_tweet_df()

    def test_find_statuses_count(self):
        self.assertEqual(
            self.df.find_statuses_count(), [8097, 5831, 1627, 1627, 18958]
        )

    def test_find_full_text(self):
        text = ['Extra random image (I):\n\nLets focus in one very specific zone of the western coast -&gt; Longjing District, Taichung #City, #Taiwan \n \n#Copernicus #Sentinel2 🛰️ 2022-08-03 \nFull Size -&gt; https://t.co/39IOoqJZR9 🧐 https://t.co/rdf21paD5P',
 "#China's media explains the military reasons for each area of the drills in the #Taiwan Strait\n\nRead the labels in the pictures ⬇️ Via CGTN https://t.co/0J4ilou4iv",
 "China even cut off communication, they don't anwer phonecalls from the US. But here clown @ZelenskyyUa enters the stage to ask #XiJinping to change Putin's mind.",
 "Putin to #XiJinping : I told you my friend, Taiwan will be a vassal state, including nukes, much like the Ukrainian model. I warned you... But it took Pelosi to open China's eyes.",
 'I’m sorry, I thought Taiwan was an independent country because it had its own government, currency, military, travel documents, Olympic team etc. while the PRC was a gangster regime run by a bunch of communist bandits. I apologize for the confusion. #taiwan https://t.co/j4rM8cDdD8']

        self.assertEqual(self.df.find_full_text(), text)

    def test_find_sentiments(self):
        self.assertEqual(
            self.df.find_sentiments(self.df.find_full_text()),
            (
                ([Sentiment(polarity=-0.030000000000000006, subjectivity=0.2625),
                    Sentiment(polarity=-0.1, subjectivity=0.1),
                    Sentiment(polarity=0.0, subjectivity=0.0),
                    Sentiment(polarity=0.1, subjectivity=0.35),
                    Sentiment(polarity=-6.938893903907228e-18, subjectivity=0.55625)]
                )
                [-0.030000000000000006, -0.1, 0.0, 0.1, -6.938893903907228e-18],
                [0.2625, 0.1, 0.0, 0.35, 0.55625],
            ),
        )


    def test_find_screen_name(self):
        name = ['i_ameztoy', 'ZIisq', 'Fin21Free', 'Fin21Free', 'VizziniDolores']
        self.assertEqual(self.df.find_screen_name(), name)

    def test_find_followers_count(self):
        f_count = [20497, 65, 85, 85, 910]
        self.assertEqual(self.df.find_followers_count(), f_count)

    def test_find_friends_count(self):
        friends_count = [2621, 272, 392, 392, 2608]
        self.assertEqual(self.df.find_friends_count(), friends_count)

    def test_find_is_sensitive(self):
        self.assertEqual(self.df.is_sensitive(), ['', '', '', '', ''])


    def test_find_hashtags(self):
        hashtags = [[{'text': 'City', 'indices': [132, 137]}],\
            [{'text': 'China', 'indices': [18, 24]},{'text': 'Taiwan', 'indices': [98, 105]}],\
            [{'text': 'XiJinping', 'indices': [127, 137]}],[{'text': 'XiJinping', 'indices': [9, 19]}],[]]
        self.assertEqual(self.df.find_hashtags(), hashtags)

    def test_find_mentions(self):
        mentions =[[{'screen_name': 'i_ameztoy','name': 'Iban Ameztoy','id': 3418339671,'id_str': '3418339671','indices': [3, 13]}],[{'screen_name': 'IndoPac_Info','name': 'Indo-Pacific News - Watching the CCP-China Threat','id': 844136511079559168,'id_str': '844136511079559168','indices': [3, 16]}],[{'screen_name': 'ZelenskyyUa','name': 'Володимир Зеленський','id': 1120633726478823425,'id_str': '1120633726478823425','indices': [90, 102]}],[],[{'screen_name': 'ChinaUncensored','name': 'China Uncensored','id': 833100331,'id_str': '833100331','indices': [3, 19]}]]
        self.assertEqual(self.df.find_mentions(),mentions)



if __name__ == "__main__":
    unittest.main()

