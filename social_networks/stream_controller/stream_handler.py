from social_networks.twitter_controller.twitter_api import Tweets
from social_networks.stream_controller.stream_parser import TweetStreamParser


class TweetStreamHandler(Tweets):
    def __init__(self, filters):
        super().__init__()
        self.stream = self.api.GetStreamFilter(track=filters)
        self.parser = TweetStreamParser

    def kill_stream(self):
        self.stream.__delete__(self)

    def pass_tweets(self):
        for tweet in self.stream:
            self.parser.parse(tweet)


if __name__ == "__main__":
    filters = ['gop', 'government shutdown', 'DACA']
    sh = TweetStreamHandler(filters)
