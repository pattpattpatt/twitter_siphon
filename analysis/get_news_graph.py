from controllers.news_site_controller import NewsSite
from data.db_interface.read import ReadFromDatabase
from itertools import combinations

#List of all the screen names of the twitter accounts of our chosen news sites
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



def get_graph_from_sites():
    #for each screen_name, create news site
    for site in NEWS_SITES:
        print("{}\n".format(site))
        NewsSite(screen_name=site).create()

    #get all news sites
    db_sites = ReadFromDatabase('twitter_siphon', 'news_sites').simple_find(filter={})

    #Get hash of all followers of the sites
    relation_map = {}
    total_followers = 0
    for site in db_sites:
        print('{}: {}'.format(site['screen_name'], site['followers_count']))
        total_followers += site['followers_count']
        # relation_map[site['screen_name']] = NewsSite(screen_name=site['screen_name']).get_followers_list()

    print(total_followers)
    pairs = combinations(relation_map, 2)
    relations = []
    for pair in pairs:
        print("{}\n".format(pair))

        # relations.append(SiteRelation.create(origin=pair[0].key(),
        #                     destination=pair[1].key(),
        #                     num_common_followers=num_common_followers(pair[0], pair[1])))


def num_common_followers(site_a, site_b):
    pass

def save_relation(origin, destination):
    pass


if __name__ == "__main__":
    get_graph_from_sites()
