from controllers.helpers.sync_helper import SyncHelper
from pymongo.errors import *
from datetime import datetime


class SiteRelationSyncHelper(SyncHelper):
    def __init__(self, sync_obj, model):
        super().__init__(sync_obj, model)

    def sync_obj_data_with_db(self):
        # Set object's last updated time to current time
        self.set_update_time()

        update = self.collect_update()

        filter = {
            'origin_site_sn': self.sync_obj_data['origin_site_sn'],
            'destination_site_sn': self.sync_obj_data['destination_site_sn']
        }

        # Update document: If document does not exist, create document with data from update
        self.db_writer.update_record(filter=filter,
                                     update=update,
                                     upsert=True)
        return self.sync_obj_data

    def map_obj_to_model(self):
        obj_map = {}

        # for each value in the model, see if it can be translated from the object's fields
        for key, value in self.model.items():
            # If in the object dict
            if next((x for x in list(self.sync_obj_data.keys()) if x == key), None) is not None:
                obj_map[key] = self.sync_obj_data[key]

        return obj_map

    def collect_update(self):
        return {'$set': self.map_obj_to_model()}

    def get_followers_update(self):
        return {'$addToSet': {'followers': {'$each': self.sync_obj_data['new_followers']}}}

    def set_update_time(self):
        # Update the time last updated
        self.sync_obj_data['last_db_sync'] = datetime.now()



