import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import NLPmodule as Verify
import Extraction as Extract
import preprocessor as p
import pyrebase

# Configure the firebase using my projects details in firebase
config = {"apiKey": "AIzaSyAeQ7GxJ9mHgjKSsDENENuoJCSfJK8ZynI",
          "authDomain": "comsciproject-e2794.firebaseapp.com",
          "databaseURL": "https://comsciproject-e2794.firebaseio.com/",
          "projectId": "comsciproject-e2794",
          "storageBucket": "comsciproject-e2794.appspot.com",
          "messagingSenderId": "951329715541"
          }

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Set what will get taken out of the tweet when it is cleaned
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.RESERVED, p.OPT.MENTION, p.OPT.SMILEY)

# Used for the Twitter API
consumer_key = 'RUb7JdHporUSqGjIkkSs8GBRX'
consumer_secret = 'CYPdAMRhD0wqTI017aOxfeyP1utuwJGIPeOjsGKnTqsewGK0BU'
access_token = '781244550-W8clw4oyhYk7PjVoI0HJtWE5xSJFeI8I7rtGqTkX'
access_secret = '3Sf46UZ3IrInGhsfq5mdO8VgQpByvFMsdABOVbkfrzNGV'

# Get authentication and access for using Twitter API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Using Tweepy, get access to Twitters streaming and REST API
api = tweepy.API(auth)


# This class is used for the Tweepy Streaming API. Getting tweets in realtime.
class MyListener(StreamListener):
    def on_status(self, status):
        try:
            # We disregard all tweets that are just retweets
            if status.text.split()[0] == 'RT':
                pass
            else:
                # Only need tweets that mention the word flood
                if 'flood' in status.text.lower().split():
                    # First we pre-process the tweet with taking out emojis, URLS and mentions
                    cleanTweet = p.clean(status.text)
                    # Check if the tweet isn't just the word Flood and one more thing
                    if len(cleanTweet.split()) > 2:
                        print(cleanTweet)
                        # After it has been pre-processed, pass the tweet to the verification module
                        classification = Verify.verification(cleanTweet)
                        print(classification)
                        # Only care about the tweets that are classified as pos
                        if classification == 'pos':
                            # When the classification says pos, extract keywords from the tweet
                            floodInfo = Extract.extractingText(cleanTweet)
                            if len(floodInfo) > 1:
                                # For presentation only
                                try:
                                    # Put the keywords into a string in the format that is user-friendly
                                    infoString = Extract.getInformationReady(floodInfo, status.place.full_name)
                                except:
                                    infoString = Extract.getInformationReady(floodInfo, "None")
                                # Send string to the Firebase Database
                                db.push(infoString)
                        return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            print(str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


# To get training data from the past 2 weeks on Twitter
def runTrain():
    # We will append the new tweets to the training data file
    with open('trainingdata.txt', 'a') as f:
        # Query the Twitter API to search for tweets using the query flood
        for tweet in tweepy.Cursor(api.search, q="flood", lang='en').items():
            try:
                checkTweet = tweet.text.split()
                if checkTweet[0] == 'RT':
                    pass
                else:
                    # Clean the tweet then write the tweet to file
                    f.write(p.clean(tweet.text) + '\n')
            except:
                pass


# This function runs the Tweepy streaming portion of this module which retrieves tweets inside the bounding box of Australia
def runStream():
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(locations=[112.1, -43.9, 156.9, -9.3], track=['flood'], languages=["en"])


runStream()
# runTrain()
