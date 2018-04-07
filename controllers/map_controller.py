"""
MapController is responsible for coordinating the continuous updating
of the news sites and the site_relation objects.
"""

# Local package imports
from data.twitter_interface.twitter_api import *
from controllers.news_site_controller import NewsSiteController
from data.db_interface import *
from data.Utility import threaded
from helpers.rate_limit_helper import RateLimitHelper

# Foreign package imports
import sched
import time
from twitter.error import TwitterError

# Constants
RATE_LIMIT_PERIOD = 900.00  # 900 seconds = 15 minutes
RATE_LIMIT_TOTAL = 15.00    # Total of 15 queries per period
RATE_LIMIT_BUFFER = 0.5     # Small buffer to add sufficient padding to the delay


class MapController:
    def __init__(self, screen_names=None):
        self.api = Tweets().api
        self.writer = WriteToDatabase('twitter_siphon', 'news_sites')
        self.reader = ReadFromDatabase('twitter_siphon', 'news_sites')
        self.sites = self._init_sites_state(screen_names=screen_names)
        self.rate_limit_helper = RateLimitHelper()
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def update_map(self):
        self.update_sites()
        # self.update_site_relations()

    @threaded
    def update_sites(self):
        while True:
            for site_name in self.sites:
                try:
                    self.sites[site_name].update_followers()
                    time.sleep((RATE_LIMIT_PERIOD/RATE_LIMIT_TOTAL) + RATE_LIMIT_BUFFER)
                except TwitterError:
                    # wait ~ 15 minutes for Rate Limit to reset
                    time.sleep(RATE_LIMIT_TOTAL + RATE_LIMIT_BUFFER)

    def update_site_relations(self):
        pass

    def _init_sites_state(self, screen_names=None):
        # Ensure Correct Input
        if screen_names is None:
            return -1

        init_sites = {}  # dict to return

        for site in screen_names:
            init_sites[site] = NewsSiteController(screen_name=site)

        return init_sites

    def _init_site_relations_state(self, screen_names=None):
        pass
