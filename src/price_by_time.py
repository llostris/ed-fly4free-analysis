from collections import defaultdict
from datetime import datetime

from data_tools import get_column
from dataloaders.data_loader import TIME_KEY, PRICE_KEY
from dataloaders.json_data_loader import JsonDataLoader
from matplotlib import pyplot as plt
from time_analysis import get_num_from_time, get_time_labels

import numpy as np

def get_bin(time_in_minutes):
    return int(np.floor(time_in_minutes / 30))

def map_to_bins(times_and_prices, number_of_bins):
    time_bins = [ [] for i in range(number_of_bins + 1) ]
    for time, prices in times_and_prices:
        time_bins[get_bin(time)] += prices
    return time_bins

if __name__ == "__main__":

    data_loader = JsonDataLoader(['../data/offers2.json',
                                  # '../data/offers2.json',
                                  # '../data/offers3.json',
                                  # '../data/offers4.json'
                                  ])
    data_loader.load()

    number_of_bins = 47

    times_per_offer = [ offer[TIME_KEY] for offer in data_loader.offers ]
    times_mapped = [ datetime.strptime(x, "%H:%M") for x in times_per_offer ]
    times_mapped = [ get_num_from_time(x) for x in times_mapped ]

    prices_per_offer = [offer[PRICE_KEY] for offer in data_loader.offers]

    times_and_prices = zip(times_mapped, prices_per_offer)

    bins_to_prices = map_to_bins(times_and_prices, number_of_bins)
    bins_to_prices = list(map(lambda x: np.mean(x) if len(x) > 0 else 0, bins_to_prices))
    print(bins_to_prices)

    time_labels = get_time_labels(number_of_bins + 1, 30)

    fig, ax = plt.subplots()
    plt.plot(bins_to_prices, '*-')
    plt.xticks(range(number_of_bins + 2), time_labels, rotation=45, rotation_mode="anchor", ha="right")
    plt.title("Average price depending on time the offer was posted")
    plt.xlabel("Time of day [HH:mm]")
    plt.ylabel("Average price [PLN]")
    plt.show()
