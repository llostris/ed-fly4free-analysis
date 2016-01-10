# -*- coding: utf-8 -*-
from collections import defaultdict
from matplotlib import pyplot as plt

import data_tools

from dataloaders.data_loader import DESTINATION_KEY, DATE_KEY, CITY_KEY, COUNTRY_KEY, PRICE_KEY
from dataloaders.json_data_loader import JsonDataLoader
from parsers.date_parser import DateParser
from price_analysis import PriceAnalysisEntity, sort_by_property


date_parser = DateParser()
RESULTS_DIR = '../results/'


def group_by_property(offers, property):
    results = defaultdict(list)
    for offer in offers:
        if property == 'month':
            results[offer[DATE_KEY].month].append(offer)
        else:
            results[offer[property]].append(offer)
    return results


def group_by_price(offers, property):
    results = defaultdict(list)
    for offer in offers:
        if len(offer[PRICE_KEY]) > 0:
            results[offer[property]] += offer[PRICE_KEY]
    print(results)

    mapped = list(map(lambda x: PriceAnalysisEntity(property, x, results[x]), results))
    for entity in mapped:
        entity.calculate_values()

    return mapped


def sort_by_month(offers_by_destination, reverse=False):
    sorted_offers = {}
    for destination in offers_by_destination:
        offers = offers_by_destination[destination]
        sorted_offers[destination] = sorted(offers, key = lambda x: x[DATE_KEY].month, reverse = reverse)
    return sorted_offers


def plot_number_of_offers_by_months(offers_by_destination):
    grouped_by_month = group_by_property(offers_by_destination, 'month')
    results = []
    for month in grouped_by_month:
        results.append((month, len(grouped_by_month[month])))

    # print(results)

    labels = date_parser.get_month_labels_for_plot(grouped_by_month)
    # print(labels)

    plt.plot(data_tools.get_column(results, 0), data_tools.get_column(results, 1))
    plt.xticks(data_tools.get_column(labels, 0), data_tools.get_column(labels, 1), rotation=45, rotation_mode="anchor", ha="right")
    data_tools.set_plot_settings('Number of offers per month', 'Months', 'Number of offers')
    plt.savefig('../results/number_of_offers_by_months.png')
    # plt.show()


def destination_prices_by_months(offers_by_destination, property, top=50):
    grouped_by_month = group_by_property(offers_by_destination, 'month')
    results = []
    for month in grouped_by_month:
        prices_per_destination = group_by_price(grouped_by_month[month], property)
        prices_per_destination = sort_by_property(prices_per_destination, 'average')
        results.append((month, prices_per_destination[:top]))
    # print(results)

    labels = date_parser.get_month_label(grouped_by_month)

    with open('../results/country_prices_by_month.txt', 'w+', encoding = 'utf-8') as f:
        for month, prices_per_destination in results:
            f.write(labels[month])
            f.write('\n')
            f.write(PriceAnalysisEntity.get_data_header())
            f.write('\n')

            for prices in prices_per_destination:
                f.write(prices.get_formatted_row())
                f.write('\n')

            f.write('\n')

    return results


def popular_destinations_by_month(offers_by_destination, property, top=50, save_to_file=True):
    grouped_by_month = group_by_property(offers_by_destination, 'month')
    results = defaultdict()
    for month in grouped_by_month:
        prices_per_destination = group_by_property(grouped_by_month[month], COUNTRY_KEY)
        destination_and_offers = [ (destination, len(offers)) for destination, offers in
                                   prices_per_destination.items() ]
        destination_and_offers = sorted(destination_and_offers, key = lambda x: x[1], reverse = True)
        results[month] = destination_and_offers

    # print(results)

    labels = date_parser.get_month_label(grouped_by_month)

    if save_to_file:
        with open(RESULTS_DIR + property + '_by_month.txt', 'w+', encoding = 'utf-8') as f:
            for month, countries_and_counts in results.items():
                f.write(labels[month])
                f.write('\n-----------\n')

                for country, counts in countries_and_counts[:top]:
                    country_name = data_tools.get_objects(property).get(id=country).name
                    f.write(country_name + ' ' + str(counts))
                    f.write('\n')

            f.write('\n')

    return results


def price_in_time(offers_by_destination, property, ids=None):
    offers_by_destination = group_by_property(data_loader.offers_by_destination, COUNTRY_KEY)

    for destination in offers_by_destination:
        grouped_by_month = group_by_property(offers_by_destination[destination], 'month')
        # print(grouped_by_month)

        for month in grouped_by_month:
            grouped_by_price = group_by_price(grouped_by_month[month], property)
            grouped_by_month[month] = grouped_by_price

        offers_by_destination[destination] = grouped_by_month

    # print(offers_by_destination)

    with open(RESULTS_DIR + property + '_by_price.txt', 'w+', encoding = 'utf-8') as f:
        for destination in offers_by_destination:
            destination_name = data_tools.get_objects(property).get(id = destination)
            f.write(destination_name.name)
            f.write('\n----------\n')
            f.write('\n')
            for month in offers_by_destination[destination]:
                f.write('-' + str(month) + '-')
                f.write('\n')
                grouped_by_month = offers_by_destination[destination][month]
                for offer in grouped_by_month:
                    f.write(offer.get_formatted_row())
                    f.write('\n')

    if ids is not None:
        for id in ids:
            country_name = data_tools.get_objects(property).get(id=id).name
            average_prices = [ (month, prices[0].average) for month, prices in offers_by_destination[id].items() if
                               len(prices) > 0 ]
            labels = date_parser.get_month_labels_for_plot(offers_by_destination[id])
            # print(average_prices)

            plt.clf()
            plt.plot(data_tools.get_column(average_prices, 0), data_tools.get_column(average_prices, 1))
            plt.xticks(data_tools.get_column(labels, 0), data_tools.get_column(labels, 1), rotation=45, rotation_mode="anchor", ha="right")
            data_tools.set_plot_settings('Average prices in time for ' + country_name,
                                         'Month',
                                         'Average price [PLN]')
            # plt.show()
            plt.savefig(RESULTS_DIR + 'monthly/' + country_name + '.png')


if __name__ == "__main__":
    data_loader = JsonDataLoader(['../data/offers1.json',
                                  '../data/offers2.json',
                                  # '../data/offers3.json',
                                  # '../data/offers4.json'
                                  ])
    data_loader.load()
    data_loader.separate_offers(DESTINATION_KEY)
    data_loader.load_country_data()

    plot_number_of_offers_by_months(data_loader.offers_by_destination)

    destination_prices_by_months(data_loader.offers_by_destination, COUNTRY_KEY, top=10)

    popular_destinations_by_month(data_loader.offers_by_destination, COUNTRY_KEY, top=10)

    country_names = [ 'Włochy', 'Francja', 'Wielka Brytania', 'Hiszpania', 'Niemcy', 'Portugalia', 'Kanada' ]
    most_popular_countries_ids = [ data_tools.get_objects(COUNTRY_KEY).get(name=x).id for x in country_names ]
    print(most_popular_countries_ids)
    price_in_time(data_loader.offers_by_destination, COUNTRY_KEY, most_popular_countries_ids)