# This runs on a schedule based on the map controller's state of operation
# E.G. The map controller dispatches an instance of SiteRelationController in order to update the
# Map based on the state of the sites in the DB. This class only cares which sites are in the db,

# The basics of this class are to get the list of sites in the db,
# Get the current state of the relations based on a list of site_relation objects
# For each relation, pull the list of followers for each set of relationships
# Run the overlap checker
# Store the resulting overlap number into the db
# Run graph creator, to cache the graph of sites (and to create an index of sites in different groups)

# Imports
from data.twitter_interface.twitter_api import Tweets
from data.db_interface.write import WriteToDatabase
from data.db_interface.read import ReadFromDatabase
from datetime import datetime
from time import sleep


class SiteRelationController:
    def __init__(self, origin_site, dest_site):
        self.api = Tweets().api
        self.db_reader = ReadFromDatabase('twitter_siphon', 'news_sites')
        self.db_writer = WriteToDatabase('twitter_siphon', 'news_sites')
        self.origin_site = origin_site
        self.destination_site = dest_site

        # Initialize instance models
        self._init_instance_state(origin_site, dest_site)

    def relation_from_db(self, origin_site_id, destination_site_id):
        print('\n*** relation_from_db ***')

        filter = {'origin_site_id': origin_site_id,
                  'destination_site_id': destination_site_id}

        cursor = self.db_reader.simple_find(filter=filter, limit=1)
        print('{}'.format(cursor))
        if cursor.count() == 1:
            print('Object exists in DB as id: {}'.format(cursor[0]['_id']))
            return cursor[0]

        # If not exist in database
        elif cursor.count() == 0:
            print('{} Is not in DB')
            return None

        else:
            return None

    def update_relation(self, origin_site, destination_site):
        #Creates new relation from two sites' screen names

        pass

    def destroy_relation(self, origin, destination):
        pass

    def save(self):
        #Save all updates to the DB
        pass

    def _init_instance_state(self, origin_site_sn, destination_site_sn):

        print('*** _init_instance_state ***')

        data = {}
        # test for relation in db
        db_data = self.relation_from_db(origin_site_id=origin_site_sn, destination_site_id=destination_site_sn)

        # If site exists in db, initialize object state with that models
        # Else, get init from Twitter
        if db_data is not None:
            # print('Initializing news site from database...')
            self._init_instance_variables(db_data)

        else:
            # print('Initializing news site from twitter...\n')
            data = self.create_relation(origin_site=origin_site_sn, destination_site=destination_site_sn)
            # print('Syncing with DB...\n')
            self._init_instance_variables(data)
            self.save()

    def _init_instance_variables(self, data):
        self.origin_site_id = self.origin_site._mongo_id()
        self.destination_site_id = self.destination_site._mongo_id()
        self._init_instance_variables_from_data(data)

    def _init_instance_variables_from_data(self, data):
        self.last_db_sync = data['last_db_sync']
        self.num_common_followers = data['num_common_followers']
        self.normalized_distance = data['normalized_distance']

# db.news_sites.aggregate([ { $match : { $or : [ {'screen_name': 'TheEconomist' }, {'screen_name': 'BBC'} ]}},{ $project: {'followers':1, '_id': 0}}, {$project: {$size: 'followers'}}])