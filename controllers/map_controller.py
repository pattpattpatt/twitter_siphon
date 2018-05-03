"""
MapController is responsible for coordinating the continuous updating
of the news sites and the site_relation objects.
"""

# Local package imports
from data.twitter_interface.twitter_api import *
from controllers.news_site_controller import NewsSiteController
from data.db_interface import *
from controllers.site_relation_controller import SiteRelationController

# Foreign package imports
import sched
import time
from twitter.error import TwitterError
from itertools import combinations

# Constants
RATE_LIMIT_PERIOD = 900.00  # 900 seconds = 15 minutes
RATE_LIMIT_TOTAL = 15.00    # Total of 15 queries per period
RATE_LIMIT_BUFFER = 0.5     # Small buffer to add sufficient padding to the delay
UPDATE_CYCLES = 1           # Number of times to update the whole site list before updating the relations


class MapController:
    def __init__(self, screen_names=None):
        self.api = Tweets().api
        self.writer = WriteToDatabase('twitter_siphon', 'news_sites')
        self.reader = ReadFromDatabase('twitter_siphon', 'news_sites')
        self.sites = self._init_sites_state(screen_names=screen_names)
        self.relations = self._init_site_relations_state()
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def update_map(self):
        while True:
            # self.update_sites()
            self.update_site_relations()

    def update_sites(self):
        for cycle in range(0, UPDATE_CYCLES):
            print('UPDATING SITES - Cycle {}'.format(cycle))
            for site_name in self.sites:
                try:
                    print('\nupdating site: {}'.format(site_name))
                    self.sites[site_name].update_followers()
                    print(self.api.CheckRateLimit(url='https://api.twitter.com/1.1/followers/ids.json'))
                    time.sleep((RATE_LIMIT_PERIOD/RATE_LIMIT_TOTAL) + RATE_LIMIT_BUFFER)
                except TwitterError:
                    print('rate limit exception hit')
                    # wait ~ 15 minutes for Rate Limit to reset
                    time.sleep(RATE_LIMIT_PERIOD + RATE_LIMIT_BUFFER)


    def update_site_relations(self):
        print('UPDATING RELATIONS')
        for relation in self.relations:
            relation.update_relation()

    def _init_sites_state(self, screen_names=None):
        # Ensure Correct Input
        if screen_names is None:
            return -1

        init_sites = {}  # dict to return

        for site in screen_names:
            init_sites[site] = NewsSiteController(screen_name=site)

        return init_sites

    def _init_site_relations_state(self):
        site_combinations = combinations(self.sites.items(), 2)

        relations = []
        for comb in site_combinations:
            relations.append(SiteRelationController(origin_site=comb[0][1],
                                                    destination_site=comb[1][1]))
        return relations
