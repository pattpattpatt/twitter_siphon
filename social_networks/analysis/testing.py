from social_networks.data.news_site import NewsSite

if __name__ == '__main__':
    site = NewsSite(screen_name='Seahawks')

    followers = []
    count = 1
    while True:
        next_cursor, previous_cursor, batch = site.get_followers_list()
        print('batch number {}'.format(count))
        followers.extend([x for x in batch])
        if next_cursor == 0:
            break
        count += 1
        print('Followers Count: {}\n'.format(len(followers)))

    print('{}\n'.format(len(followers)))


#NOTE for tomorrow
# There needs to be an abstraction here since the performance bottleneck will
# be in the concurrent processing of huge amounts of information
# Is there a way to not have to store large amounts of data in memory?
# Is there a way to concurrently process separate pairs of id's?
# Should the pair-builder be abstracted into a class separate from the news_site class?
