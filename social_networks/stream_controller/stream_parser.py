from social_networks.database_controller.database import Database


class TweetStreamParser():
    def __init__(self):
        pass

    """Extracts: user ID string,
                         tweet ID,
                         tweet text,
                         hashtags,
                         links,
                         parent_tweets,
                         retweet id's,
        Returns: dictionary representing tweet document to be imported"""
    def parse_tweet(self, tweet):

        print(tweet)

    # Returns a list of hashtags, or an empty list if no hashtags
    def hashtags_from_tweet(self, tweet):
        pass

    # Returns a list of link dictionaries
    def links_from_tweet(self, tweet):
        pass

    def user_from_tweet(self):
        pass


