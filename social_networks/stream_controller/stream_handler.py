# Local Imports
from social_networks.stream_controller.stream_parser import TweetStreamParser
from social_networks.twitter_controller import __credential_file__ as twitter_cred
from social_networks.database_controller.database import Database

# Package Imports
import json
import twitter
from pymongo.operations import *


class TweetStreamHandler(Database):
    def __init__(self, stream, parser):
        super().__init__(stream['name'])
        self.stream = stream['stream']
        self.parser = parser
        self.TWEET_PAYLOAD_LIMIT = 100

    def parse_tweets_in_stream(self):
        tweet_payload = []
        for tweet in self.stream:
            tweet_payload.append(tweet)
            if len(tweet_payload) >= self.TWEET_PAYLOAD_LIMIT:
                self.collect_bulk_upload_payload(tweet_payload)
                tweet_payload.clear()

    """compiles insert commands and sends to db.bulk_upload"""
    def collect_bulk_upload_payload(self, data_payload):
        print(data_payload)
        insert_cmds = []
        for item in data_payload:
            insert_cmds.append(InsertOne(item))
        self.bulk_write('tweets', insert_cmds)
