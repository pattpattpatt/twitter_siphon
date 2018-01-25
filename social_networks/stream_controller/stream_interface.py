# Local Imports
from social_networks.stream_controller.stream_handler import TweetStreamHandler
from social_networks.stream_controller.stream_parser import TweetStreamParser
from social_networks.twitter_controller import __credential_file__ as twitter_cred

# Libraries
import json
import twitter


class TweetStreamInterface:
    def __init__(self):
        self.streams = {}
        self.api = None


    def take_input(self):
        print('****** Twitter Siphon ******\n\n')
        while True:
            cmd_list = input('>>>: ').split(' ')
            print(cmd_list)
            if cmd_list[0] == 'start':
                if self.api is None:
                    self._init_api()
                print(self.create_and_start_stream(cmd_list[1], cmd_list[2:]))
            elif cmd_list[0] == 'stop':
                if cmd_list[1] == 'api':
                    # first kill stream
                    for s in self.streams:
                        self.stop_stream(s)
                        print('Stopped stream: {}'.format(s['name']))
                    # then kill api
                    self.stop_api()

                elif cmd_list[1] == 'stream':
                    for s in self.streams:
                        if s['name'] == cmd_list[2]:
                            self.stop_stream(s)
                            print('Stopped stream: {}'.format(s['name']))
                            break
            else:
                print('Invalid Input: {} is not a valid command'.format(cmd_list[0]))

    def _init_api(self):
        auth = self.get_credentials()
        self.api = twitter.Api(
            auth['CONSUMER_KEY'],
            auth['CONSUMER_SECRET'],
            auth['OAUTH_TOKEN'],
            auth['OAUTH_TOKEN_SECRET'],
            sleep_on_rate_limit=True)

    def create_and_start_stream(self, name, filters):
        try:
            self.streams[name] = self.api.GetStreamFilter(track=filters)
            stream_dict = {'stream': self.streams[name],
                           'name': name}
            TweetStreamHandler(stream_dict, TweetStreamParser()).parse_tweets_in_stream()
            return 'Started: {}'.format(name)
        except ValueError as e:
            return e



    def stop_stream(self, stream):
        pass

    def stop_api(self):
        pass

    def get_credentials(self):
        with open(twitter_cred, 'r') as file:
            auth_keys = json.load(file)
        return auth_keys

if __name__ == '__main__':
    TweetStreamInterface().take_input()
