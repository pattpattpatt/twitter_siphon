from controllers.map_controller import MapController

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

if __name__ == '__main__':
    mc = MapController(screen_names=NEWS_SITES).update_map()
