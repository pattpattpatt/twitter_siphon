"""
Class Interface for modifying News Site representations in DB
"""

# Imports
from data.db_interface.read import ReadFromDatabase
from data.db_interface.write import WriteToDatabase
from data.twitter_interface.twitter_api import Tweets
from controllers.helpers.news_site_sync_helper import NewsSiteSyncHelper
from data.models.news_site import NewsSite

# Constants
MAX_FOLLOWERS_IN_MEMORY = 5000  # Limit on how many followers to hold in memory


class NewsSiteController:
    def __init__(self, screen_name=None, api=None):
        if api is None:
            self.api = Tweets().api
        else:
            self.api = api
        self.db_reader = ReadFromDatabase('twitter_siphon', 'news_sites')
        self.db_writer = WriteToDatabase('twitter_siphon', 'news_sites')

        # Initialize instance models
        self._init_instance_state(screen_name)

    def site_from_db(self, screen_name):
        filter = {'screen_name': screen_name}
        cursor = self.db_reader.simple_find(filter=filter, limit=1)

        # If exists in DB
        if cursor.count() == 1:
            return cursor[0]

        # If not exist in DB
        elif cursor.count() == 0:
            return None

        else:
            return None

    def site_from_twitter(self, screen_name):
        cursor = self.api.GetUser(screen_name=screen_name).AsDict()
        data = self.filter_twitter_results(cursor)
        return data

    def filter_twitter_results(self, payload):
        return {
            'name': payload['name'],
            'twitter_id': payload['id'],
            'followers_count': payload['followers_count'],
            'last_db_sync': None,
            'new_followers': [],
            'latest_cursor_saved': -1,
            'exec_state': 'update',
            'next_cursor': -1,
            'previous_cursor': 0,
        }

    def update_operation_state(self, previous_cursor, next_cursor):
        self.update_cursor_state(previous_cursor, next_cursor)
        self.update_exec_state()

    def update_cursor_state(self, previous_cursor, next_cursor):
        """ Updates the three cursors: latest_cursor_saved,
                                       next_cursor,
                                       previous_cursor """

        self.next_cursor = next_cursor
        self.previous_cursor = previous_cursor

    def update_exec_state(self):
        if self.next_cursor == 0:
            self.exec_state = 'up_to_date'

    def update_followers(self):
        """ Get one page of new followers (< 5000 ids), then either return or sync with DB if
            a) the list of followers gathered from twitter is > MAX_FOLLOWERS_IN_MEMORY or
            b) the exec state has changed to up_to_date, and there are no more followers to retrieve """

        self.get_next_followers_page()

        print('POST_UPDATE_OPERATION_STATE_DICT: {}'.format(self.__dict__))

        if len(self.new_followers) >= MAX_FOLLOWERS_IN_MEMORY:
            self.sync_with_db()
        elif self.exec_state is 'up_to_date':
            self.sync_with_db()

    def get_next_followers_page(self):
        self.new_followers.extend(self.get_followers_page())

    def get_followers_page(self):
        """ Gets the next page of followers, and updates the cursors for the object """
        next_cursor, previous_cursor, result = self.api.GetFollowerIDsPaged(screen_name=self.screen_name,
                                                                            cursor=self.next_cursor)
        print('{} | {} | {}'.format(next_cursor, previous_cursor, len(result)))
        self.update_operation_state(previous_cursor, next_cursor)
        return result

    def sync_with_db(self):
        self.__dict__ = NewsSiteSyncHelper(self, NewsSite()).sync_obj_data_with_db()
        print('POST_SYNC_DICT: {}'.format(self.__dict__))

    def find_mongo_id(self):
        return self.db_reader.simple_find({'screen_name': self.screen_name}, limit=1)[0]['_id']

    def _mongo_id(self):
        return self.find_mongo_id()

    def _init_instance_state(self, screen_name):
        # test for site in db
        db_data = self.site_from_db(screen_name=screen_name)

        # If site exists in db, initialize object state with that models
        if db_data is not None:
            self._init_instance_variables(screen_name, db_data)

        # Else, get init from Twitter
        else:
            data = self.site_from_twitter(screen_name=screen_name)
            self._init_instance_variables(screen_name, data)
            self.sync_with_db()

    def _init_instance_variables(self, screen_name, data):
        self.screen_name = screen_name
        self.name = data['name']
        self.twitter_id = data['twitter_id']
        self.last_db_sync = data['last_db_sync']
        self.exec_state = data['exec_state']
        self.next_cursor = data['next_cursor']
        self.previous_cursor = data['previous_cursor']
        self.latest_cursor_saved = data['latest_cursor_saved']
        
        # No new followers on init
        self.new_followers = []
