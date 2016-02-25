from twitter import Twitter, OAuth, TwitterHTTPError
from config import config
import os

twitter_handles = config['twitter_handles']
t = Twitter(auth=OAuth(config['oauth_token'], config['oauth_secret'],
            config['consumer_key'], config['consumer_secret']))

class TweetLoader(object):

    def __init__(self):
        self.tweet_data = {}

    def load_old_tweets(self):
        self.tweet_data = {}
        for file in os.listdir("./data"):
            if file.endswith(".csv") == False: continue
            filename = './data/' + file
            tweets = self.tweet_data[file.split('.csv')[0]] = set()
            with open(filename) as in_file:
                for line in in_file:
                    if line == '\n': break
                    tweets.add(line.replace('\n', ''))

        return self.tweet_data

    def load_tweets(self, limit=5000):
        for screen_name in twitter_handles:
            tweets = self.tweet_data[screen_name] = set()
            max_id = None
            while True:
                timeline = None
                if max_id != None:
                    timeline = t.statuses.user_timeline(screen_name=screen_name, count=200, max_id=max_id)
                else:
                    timeline = t.statuses.user_timeline(screen_name=screen_name, count=200)

                # If no more tweets, return
                if len(timeline) == 1 or len(timeline) == 0:
                    break

                # Add tweets to list
                for tweet in timeline:
                    # If Tweet Count exceeds limit return
                    if len(tweets) + 1 > limit: break
                    tweets.add(tweet['text'])

                    # store max_id for next iteration
                    max_id = tweet['id']

                # break outer loop if necessary
                if len(tweets) + 1 > limit:
                    break

        return self.tweet_data

    def save_tweets_to_disk(self):
        for key, value in self.tweet_data.iteritems():
            filename = './data/' + key + '.csv'
            with open(filename, "wb+") as out_file:
                for tweet in value:
                    out_file.write(tweet.encode('utf-8').replace('\n', '') + '\n')
