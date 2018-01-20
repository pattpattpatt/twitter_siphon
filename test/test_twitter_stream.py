import twitter
import time
from /Users/alexp5/Projects/twitter_siphon/twitter_controller/twitter_api.py import Tweets

CONSUMER_KEY = "V3tvmhL6VFetMF77EJa6hUvbE"
CONSUMER_SECRET = "0XDQhp8ZzX6ylaz6bTEqUqIABtRAXMQrFNWH9K5SXhjXESghIN"
OAUTH_TOKEN = "3193481551-fYobTrMm2OiG1j33fRPbjLI0OkzRWkz2M9qiPVl"
OAUTH_TOKEN_SECRET = "zfv77zxMyCZ2tWtES50TOlBKc3AiadYJAgvMFuKsdMObA"

api = twitter.Api(
            CONSUMER_KEY,
            CONSUMER_SECRET,
            OAUTH_TOKEN,
            OAUTH_TOKEN_SECRET,
            sleep_on_rate_limit=True)

track = [
    "NFL",
    "Patriots",
    "Championship"
]

stream = api.GetStreamFilter(track=track)

for tweet in stream:
    print('{} | {}'.format(tweet['created_at'], time.gmtime()))
