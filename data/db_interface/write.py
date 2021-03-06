from .database import Database


class WriteToDatabase(Database):

    def __init__(self, db_name, collection):
        super().__init__(db_name)
        self.collection = self.db[collection]
        self.client.close()


    def add_data(self, data):
        post_id = self.collection.insert_one(data).inserted_id
        return post_id

    def update_record(self, filter, update={}, upsert=False):
        if upsert:
            record_id = self.collection.update_one(filter=filter, update=update, upsert=upsert)
        else:
            record_id = self.collection.update_one(filter=filter, update=update)
        return record_id
