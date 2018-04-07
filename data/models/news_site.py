# Class Defines the data members of the news_site records in the db
class NewsSite:
    def __init__(self):
        self.screen_name = None
        self.name = None
        self.twitter_id = None
        self.followers = []
        self.last_db_sync = None
        self.exec_state = None
        self.next_cursor = None
        self.previous_cursor = None
        self.latest_cursor_saved = None

        #collection for this model
        self.collection = 'news_sites'
