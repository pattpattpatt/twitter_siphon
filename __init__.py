from analysis.get_news_graph import *
from data.db_interface.read import ReadFromDatabase


if __name__ == "__main__":
    create_graph(ReadFromDatabase('twitter_siphon', 'site_relations'))
