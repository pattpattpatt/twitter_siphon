from controllers.news_site_controller import NewsSiteController
from data.Utility import threaded
from controllers.map_controller import MapController
from data.twitter_interface.twitter_api import Tweets
from data.models.news_site import NewsSite
from controllers.helpers.news_site_sync_helper import NewsSiteSyncHelper
from data.db_interface.read import ReadFromDatabase
from data.db_interface.read import ReadFromDatabase
NEWS_SITES = [
    'TheEconomist',
    'BBC',
    'NPR',
    'WSJ',
    'ABC',
    'NBC',
    'USATODAY',
    'nytimes',
    'MSNBC',
    'guardian',
    'business',         # Bloomberg, because a relevant screen name is too much to ask
    'NewYorker',
    'FoxNews',
    'ForeignAffairs',
    'TheAtlantic']



@threaded
def get_follower_list(screen_name):
    site = NewsSiteController(screen_name=screen_name)

    followers = []
    count = 1
    while True:
        next_cursor, previous_cursor, batch = site.get_followers_list()
        print('batch number {}'.format(count))
        followers.extend([x for x in batch])
        if next_cursor == 0:
            break
        count += 1
        print('Followers Count: {}\n'.format(len(followers)))

    print('{}\n'.format(len(followers)))
    return followers


def test_out_of_bounds_cursor(cursor):
    result = Tweets().api.GetFollowerIDsPaged(screen_name='elonmusk', cursor=cursor)
    print(result)
def test_map_controller(sites):
    mc = MapController(sites)
    return 0

def test_news_site_sync_handler():
    ns = NewsSiteController(screen_name='BBC')
    handler = NewsSiteSyncHelper(ns, NewsSite())
    map = handler.sync_obj_data_with_db()
    print('Map: {}'.format(map))


def get_names:

if __name__ == '__main__':
    # MapController(NEWS_SITES).update_map()
    #
    # # pipeline = [
    # #     {"$match":
    # #         {"$or":
    # #             [
    # #                 {'screen_name': 'TheEconomist'},
    # #                 {'screen_name': 'BBC'}
    # #             ]
    # #         }
    # #     },
    # #     {"$group": {"_id": None,
    # #                 "followers_set": {"$push": '$followers'}
    # #                 }
    # #      },
    # #     {"$project":
    # #         {'num_common_followers':
    # #             {"$size":
    # #                 {"$setIntersection":
    # #                     [
    # #                         {"$arrayElemAt": ['$followers_set', 0]},
    # #                         {"$arrayElemAt": ['$followers_set', 1]}
    # #                     ]
    # #                 }
    # #             }
    # #         }
    # #     }
    # # ]
    # # counts = []
    # # # print(ReadFromDatabase('twitter_siphon','news_sites').aggregate(pipeline=pipeline).first)
    # # for count in ReadFromDatabase('twitter_siphon','news_sites').aggregate(pipeline=pipeline):
    # #     counts.append(count['num_common_followers'])
    # # print(counts)
    # api = Tweets().api
    #
    # total_followers = 0
    #
    # for site in NEWS_SITES:
    #     total_followers += int(api.GetUser(screen_name=site).followers_count)
    # print('Days to complete: {}'.format(float(total_followers/5000/(60*24))))

#NOTE for tomorrow
# There needs to be an abstraction here since the performance bottleneck will
# be in the concurrent processing of huge amounts of information
# Is there a way to not have to store large amounts of models in memory?
# Is there a way to concurrently process separate pairs of id's?
# Should the pair-builder be abstracted into a class separate from the news_site class?
