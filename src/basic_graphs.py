# -*- coding: utf-8 -*-
import operator
from collections import defaultdict

from data_tools import get_objects
from dataloaders.data_loader import CITY_KEY, AIRLINE_KEY, TIME_KEY, COUNTRY_KEY, SOURCES_KEY, DESTINATION_KEY
from dataloaders.json_data_loader import JsonDataLoader
from time_analysis import make_time_histogram

__author__ = 'Magda'


def most_popular(data, attribute, no_of_results=20):
    occurrences = defaultdict(int)
    for offer in data:
        if attribute == AIRLINE_KEY:
            for value in offer[attribute]:
                occurrences[value] += 1
        else:
            occurrences[offer[attribute]] += 1
    occurrences = sorted(occurrences.items(), key=operator.itemgetter(1), reverse=True)
    print(occurrences)
    objects = get_objects(attribute)
    results = [ (objects.get(id=id).name, occurrence) for (id, occurrence) in occurrences[:no_of_results] ]
    return results


def save_to_file(datalist, filename):
    with open(filename, 'w+', encoding = 'utf-8') as f:
        for entity in datalist:
            if isinstance(entity, (list, tuple)):
                for part in entity:
                    f.write(str(part))
                    f.write(' ')
            else:
                f.write(entity)
            f.write('\n')
        f.close()


if __name__ == "__main__":
    data_loader = JsonDataLoader(['../data/offers2.json',
                                  # '../data/offers2.json',
                                  # '../data/offers3.json',
                                  # '../data/offers4.json'
                                  ])
    data_loader.load()
    data_loader.separate_offers(DESTINATION_KEY)
    data_loader.separate_offers(SOURCES_KEY)
    data_loader.load_country_data()

    offers = data_loader.offers
    print('Offers: ' + str(len(offers)))
    separated_offers = data_loader.offers_by_destination

    # most popular cites and countries
    popular_cities = most_popular(separated_offers, CITY_KEY)
    save_to_file(popular_cities, '../results/popular_cities_by_destination.txt')
    popular_countries = most_popular(separated_offers, COUNTRY_KEY)
    save_to_file(popular_countries, '../results/popular_countries_by_destination.txt')

    popular_cities = most_popular(data_loader.offers_by_source, CITY_KEY)
    save_to_file(popular_cities, '../results/popular_cities_by_source.txt')
    popular_countries = most_popular(data_loader.offers_by_source, COUNTRY_KEY)
    save_to_file(popular_countries, '../results/popular_countries_by_source.txt')

    popular_airlines = most_popular(separated_offers, AIRLINE_KEY)
    save_to_file(popular_airlines, '../results/popular_airlines.txt')

    # print(popular_cities)
    # print(popular_countries)

    # time histogram
    times = [ offer[TIME_KEY] for offer in separated_offers ]
    make_time_histogram(times, 30)
