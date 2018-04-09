"""
WORK IN PROGRESS
"""

# Imports
from data.db_interface.read import ReadFromDatabase
from data.db_interface.write import WriteToDatabase


# Syncs the new followers with the DB follower list
class FollowersHelper:
    def __init__(self, screen_name, new_followers):
        self.new_followers = new_followers
        self.screen_name = screen_name
        self.reader = ReadFromDatabase('twitter_siphon', 'news_sites')
        self.writer = WriteToDatabase('twitter_siphon', 'news_sites')

        #Run the update
        self.append_followers_to_db()

    def append_followers_to_db(self):
        filter = {'screen_name': self.screen_name}
        update = {'$addToSet': {'followers': self.new_followers}}

        rtn_code = self.writer.update_record(filter=filter, update=update)
        print(rtn_code)
