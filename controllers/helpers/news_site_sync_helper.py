from controllers.helpers.sync_helper import SyncHelper
from datetime import datetime


class NewsSiteSyncHelper(SyncHelper):
    def __init__(self, site, model):
        super().__init__(site, model)

    def sync_obj_data_with_db(self):
        """
        Takes the current state of the object and runs an update on the database
        with the info from the object as the parameters
        """

        # Set object's last updated time to current time
        self.set_update_time()

        update = self.collect_update()

        #Update document: If document does not exist, create document with data from update
        self.db_writer.update_record(filter={'screen_name': self.sync_obj_data['screen_name']},
                                     update=update,
                                     upsert=True)
        #set latest cursor saved
        self.set_latest_cursor_saved()

        #delete new followers on successful db storage
        self.delete_new_followers()

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
        db_update = {'$set': self.map_obj_to_model()}
        db_update.update(self.get_followers_update())
        return db_update

    def get_followers_update(self):
        return {'$addToSet': {'followers': {'$each': self.sync_obj_data['new_followers']}}}

    def delete_new_followers(self):
        del self.sync_obj_data['new_followers'][:]

    def set_update_time(self):
        # Update the time last updated
        self.sync_obj_data['last_db_sync'] = datetime.now()

    def set_latest_cursor_saved(self):
        self.sync_obj_data['latest_cursor_saved'] = self.sync_obj_data['previous_cursor']
