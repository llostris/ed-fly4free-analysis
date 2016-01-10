# -*- coding: utf-8 -*-
"""
Creates graph in GML format
"""
import operator

import networkx as nx
from matplotlib import pyplot as plt

import data_tools
from constants import ANALYSIS_RESULTS_DIR, GML_RESULTS_DIR
from dataloaders.data_loader import DESTINATION_KEY, CITY_KEY, SOURCES_KEY, COUNTRY_KEY, PRICE_KEY, AIRLINE_KEY
from dataloaders.json_data_loader import JsonDataLoader
from date_analysis import group_by_property


def build_and_save_multigraph(offers, property, filename):
    graph = nx.MultiDiGraph()

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

            for price in offer[PRICE_KEY]:
                graph.add_edge(source_name, destination_name, attr = { 'price' : price})   #, airlines = airline_name,


    nx.write_gml(graph, GML_RESULTS_DIR + filename)

    return graph


def get_centrality(graph, filename, top=5, type='single'):
    all_results = {}

    centrality = nx.algorithms.degree_centrality(graph)
    nx.set_node_attributes(graph, 'degree-centrality', centrality)
    top_results = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
    nx.write_gml(graph, GML_RESULTS_DIR + filename.replace('txt', 'gml'))
    print(top_results[:top])
    all_results['all'] = top_results
    # plot_centrality(graph, centrality)

    centrality = nx.algorithms.in_degree_centrality(graph)
    top_results = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
    print(top_results[:top])
    all_results['in degree'] = top_results
    # plot_centrality(graph, centrality, 'In-degree centrality')

    centrality = nx.algorithms.out_degree_centrality(graph)
    top_results = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
    print(top_results[:top])
    all_results['out degree'] = top_results
    # plot_centrality(graph, centrality, 'Out-degree centrality')

    centrality = nx.algorithms.betweenness_centrality(graph, weight = 'price', endpoints = True)
    top_results = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
    print(top_results[:top])
    all_results['beetweenness'] = top_results

    if type == 'single':
        centrality = nx.algorithms.closeness_centrality(graph)
        top_results = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
        print(top_results[:top])
        all_results['beetweenness'] = top_results

        centrality = nx.algorithms.eigenvector_centrality(graph, max_iter = 1000)
        top_results = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
        print(top_results[:top])
        all_results['eigenvector'] = top_results

        # betweenness centrality - empty
        # closeness centraloty - Poland 1.0 (because of the structure of the graph)
        # eigenvalue centrality - not for multigraphs

    save_results(all_results, filename)


def save_results(all_results, filename):
    with open(ANALYSIS_RESULTS_DIR + filename, 'w+', encoding = 'utf-8') as f:
        for centrality, results in all_results.items():
            f.write(centrality + ' centrality')
            f.write('\n---------\n')

            for entity, value in results:
                if value > 0:
                    f.write('{}\t{}\n'.format(entity, value))

            f.write('\n')


def plot_centrality(graph, centrality, title):
    pos = nx.circular_layout(graph)
    # pos = nx.graphviz_layout(graph, prog="twopi", root=0)
    values = [ value for node, value in centrality.items() ]

    nodes = nx.draw_networkx_nodes(graph, pos = pos, node_color = values, cmap = plt.get_cmap('jet'),
                                   with_lables = True)
    edges = nx.draw_networkx_edges(graph, pos = pos)
    nx.draw_networkx_labels(graph, pos=pos)
    plt.sci(nodes)
    plt.colorbar()
    plt.sci(edges)
    plt.show()


if __name__ == "__main__":

    LOAD_DATA = True
    graph = None
    # property is either COUNTRY_KEY or CITY_KEY
    # property = COUNTRY_KEY
    property = CITY_KEY
    data_loader = JsonDataLoader(['../data/offers1.json',
                                 '../data/offers2.json'])

    if LOAD_DATA:
        data_loader.load()
        data_loader.separate_offers(DESTINATION_KEY)
        data_loader.load_country_data()

        graph = build_and_save_multigraph(data_loader.offers_by_destination,
                                          property,
                                 '{}_source_destination.gml'.format(property))
    else:
        with open('{}/{}_source_destination.gml'.format(GML_RESULTS_DIR, property)) as f:
            lines = f.readlines()
            graph = nx.parse_gml(lines)

    # all data
    get_centrality(graph, property + '_centralities.txt', top = 100,type = 'multi')

    # month by month
    if LOAD_DATA:
        by_month = group_by_property(data_loader.offers_by_destination, 'month')
        for month in by_month:
            print(month)
            graph = build_and_save_multigraph(by_month[month],
                                              property,
                                         '{}_source_destination_month_{}.gml'.format(property, month))
            get_centrality(graph,  '{}_source_destination_month_{}_centralities.txt'.format(property, month),
                           type = 'multi')
