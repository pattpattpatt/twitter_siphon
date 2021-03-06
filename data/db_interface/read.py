from .database import Database


class ReadFromDatabase(Database):

    def __init__(self, db_name, collection):
        super().__init__(db_name)
        self.db_name = db_name
        self.collection = self.db[collection]
        self.client.close()

    def read_distinct(self, value):
        return self.collection.distinct(value)

    def read_raw_data(self):
        return self.collection.find()

    def simple_find(self, filter, limit):
        return self.collection.find(filter=filter, limit=limit)

    def aggregate(self, pipeline):
        return self.collection.aggregate(pipeline=pipeline)

