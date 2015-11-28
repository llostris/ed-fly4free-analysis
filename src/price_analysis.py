import numpy as np
import sys

from collections import defaultdict

from matplotlib import pyplot as plt

from data_tools import get_objects, get_column
from dataloaders.data_loader import COUNTRY_KEY, PRICE_KEY, CITY_KEY, DESTINATION_KEY, SOURCES_KEY
from dataloaders.json_data_loader import JsonDataLoader


class PriceAnalysisEntity:

    def __init__(self, property, id, prices):
        self.property = property
        self.id = id
        self.prices = prices
        self.min = sys.maxsize
        self.max = 0
        self.median = 0
        self.average = 0
        self.name = get_objects(property).get(id=self.id).name

    def calculate_values(self):
        if len(self.prices) > 0:
            self.min = min(self.prices)
            self.max = max(self.prices)
            self.average = np.mean(self.prices)
            self.median = np.median(self.prices)

    @staticmethod
    def get_data_header():
        return 'Name, min, max, median, average'

    def get_formatted_row(self):
        return '%s, %d, %d, %f, %f' % (self.name, self.min, self.max, self.median, self.average)


def save_to_file(datalist, filename):
    with open(filename, 'w+', encoding = 'utf-8') as f:
        f.write(PriceAnalysisEntity.get_data_header())
        f.write('\n')

        for entity in datalist:
            f.write(entity.get_formatted_row())
            f.write('\n')
        f.close()


def get_price_grouped_by_property(offers, property):
    results = defaultdict(list)
    print(offers)
    for offer in offers:
        if len(offer[PRICE_KEY]) > 0:
            results[offer[property]] += offer[PRICE_KEY]
    print(results)

    mapped = list(map(lambda x: PriceAnalysisEntity(property, x, results[x]), results))
    for entity in mapped:
        entity.calculate_values()

    return mapped


def order_by_price(data, property, reverse=False):
    pass


def make_box_plot(data, ids=None):
    count = 0
    def get_order_and_value(x, count=count):
        count += 1
        return (count, x.name)

    if ids != None:
        data = list(filter(lambda x: x.id in ids, data))
    array_of_arrays = [ entity.prices for entity in data ]
    xlabels = [ (order + 1, entity.name) for (order, entity) in zip(range(len(data)), data) ]
    print(xlabels)
    plt.boxplot(array_of_arrays)
    plt.xticks(get_column(xlabels, 0), get_column(xlabels, 1), rotation=45, rotation_mode="anchor", ha="right")

    plt.show()


def sort_by_property(data, property, reverse=False):
    def get_property_value(x, property):
        if property == "average":
            return x.average
        elif property == "median":
            return x.median
    sorted_data = sorted(data, key = lambda x: get_property_value(x, property))
    print(sorted_data)
    return sorted_data


if __name__ == "__main__":
    data_loader = JsonDataLoader(['./data/offers1.json',
                                  # './data/offers2.json',
                                  # './data/offers3.json',
                                  # './data/offers4.json'
                                  ])
    data_loader.load()
    data_loader.separate_offers(DESTINATION_KEY)
    data_loader.separate_offers(SOURCES_KEY)
    data_loader.load_country_data()

    grouped_by_country = get_price_grouped_by_property(data_loader.offers_by_destination, COUNTRY_KEY)
    grouped_by_country = sort_by_property(grouped_by_country, "average")
    save_to_file(grouped_by_country, 'results/prices_by_country.txt')
    # print(grouped_by_country)

    grouped_by_city = get_price_grouped_by_property(data_loader.offers_by_destination, CITY_KEY)
    grouped_by_city = sort_by_property(grouped_by_city, "average")
    save_to_file(grouped_by_city, 'results/prices_by_city.txt')
    # print(grouped_by_city)

    make_box_plot(grouped_by_country, [260, 9, 11, 12])
    make_box_plot(grouped_by_country)
