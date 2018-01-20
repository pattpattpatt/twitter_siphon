from social_networks.database_controller.database import Database


class TweetStreamParser(Database):
    def __init__(self):
        super().__init__('siphon_lake')

    def parse(self, tweet):
        print(tweet)
