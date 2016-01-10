import networkx as nx

import data_tools
from constants import GML_RESULTS_DIR, CFINDER_RESULTS_DIR
from dataloaders.data_loader import CITY_KEY, SOURCES_KEY, COUNTRY_KEY, DESTINATION_KEY, PRICE_KEY
from dataloaders.json_data_loader import JsonDataLoader
from date_analysis import group_by_property
from networks.source_destination_multigraph import get_centrality


def build_and_save_graph(offers, property, filename):
    graph = nx.DiGraph()

    db_objects = data_tools.get_objects(property)
    # airline_objects = data_tools.get_objects(AIRLINE_KEY)

    for offer in offers:
        for source in offer[SOURCES_KEY]:
            source_name, destination_name = None, None

            if property == CITY_KEY:
                source_name = db_objects.get(id=source).name
                destination_name = db_objects.get(id=offer[DESTINATION_KEY]).name
            elif property == COUNTRY_KEY:
                source_name = 'Polska'
                destination_name = db_objects.get(id=offer[COUNTRY_KEY]).name
            # print(offer[AIRLINE_KEY])
            if graph.has_edge(source_name, destination_name):
                attributes = graph.get_edge_data(source_name, destination_name)
                attributes['weight'] += 1
                graph.add_edge(source_name, destination_name, attributes)
            else:
                graph.add_edge(source_name, destination_name, { 'weight' : 1})

    # graph.ed
    nx.write_gml(graph, GML_RESULTS_DIR + filename)
    #
    return graph


def save_for_cfinder(graph, filename):
    with open(CFINDER_RESULTS_DIR + filename, 'w+') as f:
        for edge in graph.edges():
            attributes = graph.get_edge_data(edge[0], edge[1])
            f.write('"{}" "{}" {}\n'.format(edge[0], edge[1], attributes['weight']))


if __name__ == "__main__":

    graph = None
    # property is either COUNTRY_KEY or CITY_KEY
    # property = COUNTRY_KEY
    property = CITY_KEY
    data_loader = JsonDataLoader(['../data/offers1.json',
                                 '../data/offers2.json'])

    data_loader.load()
    data_loader.separate_offers(DESTINATION_KEY)
    data_loader.load_country_data()

    graph = build_and_save_graph(data_loader.offers_by_destination,
                             property,
                             'single_{}_source_destination.gml'.format(property))
    save_for_cfinder(graph, 'single_{}_source_destination.txt'.format(property))

    get_centrality(graph, 'single_{}_centralities.txt'.format(property), top=100, type='single')


    by_month = group_by_property(data_loader.offers_by_destination, 'month')
    for month in by_month:
        print(month)
        graph = build_and_save_graph(by_month[month],
                                          property,
                                     'single_{}_source_destination_month_{}.gml'.format(property, month))
        get_centrality(graph,  'single_{}_source_destination_month_{}_centralities.txt'.format(property, month))

    print('Is bipartite: ' + str(nx.is_bipartite(graph)))