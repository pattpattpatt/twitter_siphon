from social_networks.data.news_site import NewsSite
from social_networks.data.site_relation import SiteRelation
from social_networks.database_controller.read import ReadFromDatabase
from itertools import combinations

#List of all the screen names of the twitter accounts of our chosen news sites
NEWS_SITES = [
    'TheEconomist',
    'BBC',
    'BBCWorld',
    'BBCBreaking',
    'BBCScienceNews',
    'NPR',
    'PBS',
    'WSJ',
    'ABC',
    'CBS',
    'NBC',
    'CNN',
    'USATODAY',
    'googlenews',
    'nytimes',
    'washingtonpost',
    'MSNBC',
    'guardian',
    'business',         # Bloomberg, because a relevant screen name is too much to ask
    'NewYorker',
    'YahooNews',
    'FoxNews',
    'Huffington',
    'ForeignAffairs',
    'TheAtlantic']



def get_graph_from_sites():
    #for each screen_name, create news site
    for site in NEWS_SITES:
        print("{}\n".format(site))
        NewsSite(screen_name=site).create()

    #get al news sites
    db_sites = ReadFromDatabase('twitter_siphon', 'news_sites').simple_find(filter={})

    #Get hash of all followers of the sites
    relation_map = {}
    for site in db_sites:
        relation_map[site['screen_name']] = NewsSite(screen_name=site['screen_name']).get_followers_list()

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
