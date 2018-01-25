from pymongo import MongoClient


class Database:

    def __init__(self, db_name):
        from social_networks.database_controller.config import config_file
        try:
            user = config_file[db_name]['USER']
            pwd = config_file[db_name]['PWD']
            url = config_file[db_name]['URL']
        except KeyError:
        # uh oh. This config doesn't exist. Create db
            print("DB doesn't exist in config.")
            return


        config = {'user': user, 'pwd': pwd, 'url':url, 'db_name': db_name}

        mongo_string = "mongodb://{user}:{pwd}@{url}/{db_name}".format(**config)
        self.client = MongoClient(mongo_string, connect=False)
        self.db = self.client[db_name]

        # self.collection = self.db.tweet_collection

    def close(self):
        self.client.close()

    def create_collection(self, collection_name):
        self.db.create_collection(collection_name)

    def remove_collection(self, collection_name):
        """Dangerous, only use this if intending to permanently delete a collection."""
        self.db.drop_collection(collection_name)

    def collect_stats(self):
        # print(self.db.command("collstats", "new"))
        pass

    def collections(self):
        return self.db.collection_names()

    def search_collection_name(self, name):
        pass

    """Creates a bulk upload based on list of write operations"""
    def bulk_write(self, collection_name, request_payload):
        if collection_name == 'tweets':
            return self.db.tweets.bulk_write(request_payload, ordered=False)
        elif collection_name == 'users':
            return self.db.users.bulk_write(request_payload, ordered=False)
        elif collection_name == 'links':
            return self.db.links.bulk_write(request_payload, ordered=False)
        else:
            return None

if __name__ == "__main__":
    db = Database('twiter_test')
    # db.collections()
