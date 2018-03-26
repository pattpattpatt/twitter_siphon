from social_networks.twitter_controller.twitter_api import Tweets
from social_networks.database_controller.write import WriteToDatabase
from social_networks.database_controller.read import ReadFromDatabase
from datetime import datetime
from time import sleep

# Singleton Class Interface for News Site representation in DB
class NewsSite:
    def __init__(self, screen_name = None, associated_sites = None):
        self.api = Tweets().api
        self.db_reader = ReadFromDatabase('twitter_siphon', 'news_sites')
        self.db_writer = WriteToDatabase('twitter_siphon', 'news_sites')
        self.screen_name = screen_name
        self.follower_count = None
        self.last_updated = None
        self.create()

    def create(self):
        # # If exists in DB, return record
        # site = self.find(self.screen_name)
        # print("{}\n".format(site.count()))
        # if site.count() == 0:
        #     self.follower_count = site['follower_count']
        #     self.last_updated = site['last_updated_at']

        #Else, collect profile from Twitter
        site = self.api.GetUser(screen_name=self.screen_name).AsDict()
        #Add profile to db
        db_writer = WriteToDatabase('twitter_siphon', 'news_sites')
        db_writer.add_data(site)
        self.db_writer.update_record(filter={'screen_name': self.screen_name}, update={"$set": {'last_updated': datetime.now()}})

        #Update object values
        self.follower_count = site['followers_count']
        self.last_updated = datetime.now()

    def destroy(self, twitter_id, screen_name = None):
        #Defaults to twitter_id if screen_name = None. If screen_name != None, use screen_name instead
        pass

    def find(self, screen_name, mongo_id = None):
        return self.db_reader.simple_find(filter={'screen_name': screen_name})

    def update_relationship(self, relations_twitter_id):
        #Get followers last updated from news site with relations_twitter_id

        #if > than 1 week since last updated
            #if > 1000 new followers
                #get new betweenness coefficient and save it in the correct SiteRelation instance
        pass

    def get_followers_list(self):
        while True:
            rl = self.api.CheckRateLimit(url='https://api.twitter.com/1.1/followers/ids.json?')
            if rl[1] == 1:
                break
            print(rl[2])
            sleep(5)

        return self.api.GetFollowerIDsPaged(screen_name=self.screen_name)
