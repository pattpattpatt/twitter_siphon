from controllers.news_site_controller import NewsSite
from data.db_interface.read import ReadFromDatabase
from itertools import combinations
from data.db_interface.read import ReadFromDatabase
# from graph_tool.all import *

NEWS_SITES = [
    'TheEconomist',
    'BBC',
    'NPR',
    'WSJ',
    'ABC',
    'NBC',
    'USATODAY',
    'nytimes',
    'MSNBC',
    'guardian',
    'business',         # Bloomberg, because a relevant screen name is too much to ask
    'NewYorker',
    'FoxNews',
    'ForeignAffairs',
    'TheAtlantic']

def get_site_relations(reader):
    raw_data = reader.read_raw_data()
    return filter_data(raw_data)


def filter_data(raw_data):
    filtered_data = []

    for relation in raw_data:
        temp_dict = {
            'origin': relation['origin_site_sn'],
            'destination': relation['destination_site_sn'],
            'distance': relation['normalized_distance']
        }
        filtered_data.append(temp_dict)
    return filtered_data


# def create_graph(reader):
#     site_relations = get_site_relations(reader=reader)
#
#     g = Graph(directed=False)
#
#     #property maps
#     vprop = g.new_vertex_property("string")
#     g.vertex_properties['name'] = vprop
#     eprop = g.new_edge_property("float")
#     g.edge_properties['distance'] = eprop
#
#     for site in NEWS_SITES:
#         v = g.add_vertex()
#         g.vp.names[v] = site
#
#     for relation in site_relations:
#         origin = None
#         destination = None
#
#         for v in g.vertices():
#             if v.vp.name == relation['origin']:
#                 origin = v
#             elif v.vp.name == relation['destination']:
#                 destination = v
#
#             if origin is not None and destination is not None:
#                 break
#
#         e = g.add_edge(origin, destination)
#         g.ep.distance[e] = relation['distance']
#
#     return g

def get_local_nodes(node, reader):
    local_nodes = {}
    site_relations = get_site_relations(reader=reader)
    #Find all relations which include this node
    for relation in site_relations:
        if relation['origin'] == node:
            local_nodes[relation['destination']] = round(relation['distance'], 5)
        elif relation['destination'] == node:
            local_nodes[relation['origin']] = round(relation['distance'], 5)

    return local_nodes

def get_closest_connections(reader, count = 10):
    pipeline = [
        { "$sort": { "normalized_distance": -1 } }
    ]
    site_relations = reader.aggregate(pipeline=pipeline)

    count = 0
    for site in site_relations:
        if count >= 10:
            break

        print('{} and {}: {}'.format(site['origin_site_sn'],
                                     site['destination_site_sn'],
                                     round(site['normalized_distance'],5)))
        count += 1


def get_sorted_nodes(node_dict):
    sorted_keys = sorted(node_dict, key=node_dict.__getitem__)
    sorted_dict = {}

    for key in sorted_keys:
        sorted_dict[key] = node_dict[key]

    return sorted_dict


def sites_map(reader):
    sites_map = {}

    for site in NEWS_SITES:
        sites_map[site] = get_sorted_nodes(get_local_nodes(site, reader=reader))

    return sites_map


def print_sites_map(sites_map):
    for origin, locals in sites_map.items():
        print('\t{}\n***********************\nneighbor\tdistance\n----------------------------------'.format(origin))
        for site, distance in locals.items():
            print('{}:\t{}'.format(site, distance))

        print('\n')


if __name__ == "__main__":
    reader = ReadFromDatabase('twitter_siphon', 'site_relations')

    # print_sites_map(sites_map(reader))
    get_closest_connections(reader=reader)