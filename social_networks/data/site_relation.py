class SiteRelation:
    def __init__(self):
        self.num_common_followers = None
        self.normalized_distance = None
        self.origin_site = None
        self.destination_site = None

    def create(self, origin, destination, num_common_followers):
        pass

    def destroy(self, origin, destination):
        pass

    def find(self, origin, destination = None):
        #default, find all relations with given origin

        #with specified destination, return instance of SiteRelation
        pass

    def save(self):
        #Save all updates to the DB
        pass