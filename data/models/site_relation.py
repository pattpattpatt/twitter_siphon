class SiteRelation:
    def __init__(self):
        self.origin_site_sn = None
        self.destination_site_sn = None
        self.last_db_sync = None
        self.num_common_followers = 0
        self.normalized_distance = 1

        self.collection = 'site_relations'



