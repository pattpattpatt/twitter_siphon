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
from data.models.site_relation import SiteRelation
from controllers.helpers.site_relation_sync_helper import SiteRelationSyncHelper
from datetime import datetime
from time import sleep


class SiteRelationController:
    def __init__(self, origin_site, destination_site):
        self.api = Tweets().api
        self.site_reader = ReadFromDatabase('twitter_siphon', 'news_sites')
        self.relations_reader = ReadFromDatabase('twitter_siphon', 'site_relations')  # Reads from the news sites collection
        self.relations_writer = WriteToDatabase('twitter_siphon', 'site_relations')
        self.origin_site_sn = origin_site.screen_name
        self.destination_site_sn = destination_site.screen_name
        self.num_common_followers = 0
        self.normalized_distance = 1
        self.last_db_sync = None

        #create relation in db if not exists
        self.create_relation()

    def site_from_db(self):
        filter = {'origin_site_sn': self.origin_site_sn,
                  'destination_site_sn': self.destination_site_sn}

        cursor = self.relations_reader.simple_find(filter=filter, limit=1)

        # If exists in DB
        if cursor.count() == 1:
            return True

        # If not exist in DB
        elif cursor.count() == 0:
            return None

        else:
            return None

    def create_relation(self):
        if self.site_from_db() is None:
            print('creating site_relation: {}_{}'.format(self.origin_site_sn, self.destination_site_sn))
            self.num_common_followers = self.update_num_common_followers(origin_sn=self.origin_site_sn,
                                                                         destination_sn=self.destination_site_sn)
            self.sync_with_db()

    def update_relation(self):
        # print('updating site_relation: {}_{}'.format(self.origin_site_sn, self.destination_site_sn))
        #Creates new relation from two sites' screen names
        self.num_common_followers = self.update_num_common_followers(origin_sn=self.origin_site_sn,
                                                                     destination_sn=self.destination_site_sn)
        self.normalized_distance = self.normalize_relation_distance(distance=self.num_common_followers)
        self.sync_with_db()
        # print(self.__dict__)

    def sync_with_db(self):
        self.__dict__ = SiteRelationSyncHelper(self, SiteRelation()).sync_obj_data_with_db()

    def update_num_common_followers(self, origin_sn, destination_sn):
        pipeline = self.common_follower_pipeline(origin_sn,
                                                 destination_sn)

        for result in self.site_reader.aggregate(pipeline=pipeline):
            new_common_followers = result['num_common_followers']
        return new_common_followers

    def common_follower_pipeline(self, origin_sn, destination_sn):
         return [
                  {"$match":
                    {"$or":
                      [
                        {'screen_name': origin_sn},
                        {'screen_name': destination_sn}
                      ]
                    }
                  },
                  {"$group": {"_id": None,
                              "followers_set": {"$push": '$followers'}
                             }
                   },
                  {"$project":
                    {'num_common_followers':
                      {"$size":
                        { "$setIntersection":
                          [
                              {"$arrayElemAt": ['$followers_set', 0]},
                              {"$arrayElemAt": ['$followers_set', 1]}
                          ]
                        }
                      }
                    }
                  }
                ]

    def max_followers_pipeline(self):
        return [
            {"$group": {"_id": None,
                        "max_common_followers":
                            {"$max": '$num_common_followers'}
                       }
             },
            {"$project": {'max_common_followers': 1}}
        ]

    def min_followers_pipeline(self):
        return [
            {"$group": {"_id": None,
                        "min_common_followers":
                            {"$min": '$num_common_followers'}
                        }
             },
            {"$project": {'min_common_followers': 1}}
        ]

    def normalize_relation_distance(self, distance):
        """
        This normalization function takes the raw followers in common,
        Converts it into a decimal proportional to the range of followers in common for the whole map, and
        Inverts it in order to make the maximum followers in common, the shortest distance
        """
        distance = int(distance)
        range_max = self.max_followers_count()
        range_min = self.min_followers_count()

        ranged_distance = (distance - range_min)/(range_max - range_min)

        #invert distance
        normalized_distance = 1 - ranged_distance

        return normalized_distance
    
    def max_followers_count(self):
        max_common_followers = 0
        pipeline = self.max_followers_pipeline()
        for result in self.relations_reader.aggregate(pipeline=pipeline):
            max_common_followers = result['max_common_followers']
        return max_common_followers

    def min_followers_count(self):
        min_common_followers = 0
        pipeline = self.min_followers_pipeline()
        for result in self.relations_reader.aggregate(pipeline=pipeline):
            min_common_followers = result['min_common_followers']
        return min_common_followers
