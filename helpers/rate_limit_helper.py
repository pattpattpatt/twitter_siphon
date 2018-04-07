from data.twitter_interface.twitter_api import Tweets

class RateLimitHelper:
    def __init__(self):
        self.api = Tweets().api

    def get_rate_limit_time_left(self, endpoint):
        return self.api.CheckRateLimit(url=endpoint)
