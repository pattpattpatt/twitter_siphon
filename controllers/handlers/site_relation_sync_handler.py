from controllers.handlers.sync_handler import SyncHandler


class SiteRelationSyncHandler(SyncHandler):
    def __init__(self, sync_obj, model):
        super().__init__(sync_obj, model)

    def sync_obj_with_db(self, ):
        pass