from twitter.models import User

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
        return {
            '_id': tweet['id_str'],
            'usr_id': tweet['user']['id_str'],
            'text': tweet['text'],
            'hashtags': self.hashtags_from_tweet(tweet),
            'links': self.links_from_tweet(tweet),
            'in_reply_to_status_id': tweet['in_reply_to_status_id_str'],
            'created_at': tweet['created_at']}

    # Returns a list of hashtags, or an empty list if no hashtags
    def hashtags_from_tweet(self, tweet):
        return [tag['text'] for tag in tweet['entities']['hashtags']]

    # Returns a list of link dictionaries
    def links_from_tweet(self, tweet):
        return [{'short_url': url['url'], 'full_url': url['expanded_url']} for url in tweet['entities']['urls']]

    def parse_user(self, user):
        return {
            '_id': str(user['id']),
            'following': user['following'] if 'following' in user else [],
            'pop_tweets': [],
            'num_pop_tweets': 0
        }




