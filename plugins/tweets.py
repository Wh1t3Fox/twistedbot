import time
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from ConfigParser import SafeConfigParser


parser = SafeConfigParser()
parser.read('config.ini')
auth= OAuthHandler(parser.get('twitter', 'CONSUMER_KEY'), parser.get('twitter', 'CONSUMER_SECRET'))
auth.set_access_token(parser.get('twitter', 'ACCESS_KEY'),parser.get('twitter', 'ACCESS_SECRET'))
api = tweepy.API(auth)

class TweetListener(StreamListener):

    def __init__(self, bot, api=None):
        super(TweetListener, self).__init__()
        self.bot = bot

    def on_status(self, data):
        self.bot.msg('#'+parser.get('irc', 'channel'), data.text.encode('utf-8').strip())

    def on_error(self, status):
        print status


def get_tweets(bot):
    twitterstream = Stream(auth, TweetListener(bot))
    twitterstream.filter(follow=['1649256163'])
