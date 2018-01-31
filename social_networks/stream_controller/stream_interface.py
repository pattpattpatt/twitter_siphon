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

    def take_input(self, cmd_list):
        args = cmd_list['args'].split(',')
        if cmd_list['task'] == 'start':
            if self.api is None:
                self._init_api()
            return self.create_and_start_stream(cmd_list['name'], args)
        elif cmd_list['task'] == 'stop':
            return self.stop_stream(cmd_list['name'], cmd_list['mode'], args)
        else:
            return 'Invalid Input: {} is not a valid command'.format(cmd_list['task'])

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
            TweetStreamHandler(stream_dict, TweetStreamParser(), self.api).parse_and_upload_stream()
            return 'Started: {}'.format(name)
        except ValueError as e:
            print(e)



    def stop_stream(self, name, mode, args):
        if mode == 'api':
            # first kill stream
            for s in self.streams:
                self.stop_stream(s)
                print('Stopped stream: {}'.format(s['name']))
            # then kill api
            self.stop_api()
            return 'Success! Killed {}'.format(args[0])

        elif mode == 'stream':
            try:
                self.stop_stream(name)
            except TypeError as te:
                raise te

    def stop_api(self):
        pass

    def get_credentials(self):
        with open(twitter_cred, 'r') as file:
            auth_keys = json.load(file)
        return auth_keys


if __name__ == '__main__':
    TweetStreamInterface().take_input()
