# Local Imports
from social_networks.twitter_controller import __credential_file__ as twitter_cred
from social_networks.database_controller.database import Database

# Package Imports
import json
import twitter
import math
from pymongo.operations import *
from pymongo.errors import BulkWriteError


class TweetStreamHandler(Database):

    def __init__(self, stream, parser, api):
        super().__init__(stream['name'])
        self.stream = stream['stream']
        self.parser = parser
        self.api = api
        self.PAYLOAD_LIMIT = 100

    def parse_and_upload_stream(self):
        tweet_payload = []
        user_list = []

        for tweet in self.stream:
            if 'text' not in tweet:
                print(tweet)
                continue

            # parse tweet and add to upload batch
            tweet_payload.append(self.parser.parse_tweet(tweet))

            # get user id's from each tweet
            user_list.append(tweet_payload[-1]['usr_id'])

            # Upload batch of tweets and clear payload
            if len(tweet_payload) >= self.PAYLOAD_LIMIT:
                self.collect_bulk_upload(tweet_payload, 'insert')
                tweet_payload.clear()

            # Handle user search and upload
            if len(user_list) >= self.PAYLOAD_LIMIT:
                self.search_and_upload_users(user_list)
                user_list.clear()

    def search_and_upload_users(self, users):
        upload_data = []

        # List of users not in DB
        needed_users = self.get_needed_users(users)
        # get and parse each user info
        for user in needed_users:
            try:
                upload_data.append(self.parser.parse_user(self.api.GetUser(user_id=user).AsDict()))
            except TypeError as te:
                print(te)
                print(user)

        # Bulk upload
        self.collect_bulk_upload(upload_data, 'upsert_users', )

    def get_needed_users(self, usr_list):
        search_list = []

        # Get list of needed users
        for user in usr_list:
            find = {'_id': user}
            if self.db['users'].find(find).count() == 0:
                search_list.append(user)

        return search_list

    """compiles insert commands and sends to db.bulk_upload"""
    def collect_bulk_upload(self, data_payload, mode, filter={}):
        #print(data_payload)
        insert_cmds = []

        # Cases for mode
        if mode == 'insert':
            for item in data_payload:
                insert_cmds.append(InsertOne(item))

            try:
                self.bulk_write('tweets', insert_cmds)
            except BulkWriteError as bwe:
                print(bwe.details)

        elif mode == 'upsert_users':
            for item in data_payload:
                insert_cmds.append(UpdateOne(filter, item, upsert=True))

            try:
                self.bulk_write('users', insert_cmds)
            except BulkWriteError as bwe:
                print(bwe.details)
