# import
from data.db_interface.write import WriteToDatabase
from data.db_interface.read import ReadFromDatabase


class SyncHelper:
    def __init__(self, sync_obj, model):
        self.sync_obj_data = sync_obj.__dict__
        self.model = model.__dict__
        self.db_reader = ReadFromDatabase('twitter_siphon', self.model['collection'])
        self.db_writer = WriteToDatabase('twitter_siphon', self.model['collection'])

    def sync_obj_data_with_db(self, ):
        pass

