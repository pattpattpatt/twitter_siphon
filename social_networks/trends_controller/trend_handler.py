class TrendHandler:
    def __init__(self):
        pass

    def dispatch_trend_search(self):
        #This is the interface function for the class
        #This is the only public function
        #When called, this will check if the wait time is up and send out a query to get the trending topics

        #Search for trends

        #For each trend
            #search for trend name
            #filter search results
                #For each tweet in results
                    #if tweet has good links, add links to list of links
                #Find best fitting set of 5 links
            #Store links in TrendView document

        pass

    def check_wait_time(self):
        pass

    def search_topic(self, topic):
        #Takes a single topic, and returns search results from Twitter
        #If Error, returns empty array
        pass

    def does_tweet_have_good_links(self, tweet):
        #Takes: a tweet and list of acceptible domains
        #Returns: list of acceptable links ([] if no links)
        pass

    def find_best_set_of_links(self, links):
        #Finds best set of 5 links out of list

        #If len(list) <= 5
            #update TrendView with each link replacing the one most closely associated with it.
            #return on successful update

        #Get distribution

        pass

    def get_set_distribution(self, links):
        #Takes: set of links
        #Returns: set of 5 links which have the most even distribution

        pass
