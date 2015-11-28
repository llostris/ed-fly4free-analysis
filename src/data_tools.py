import os

# load Django settings - must be done before loading any Django objects!
from matplotlib import pyplot as plt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Fly4FreeExplorer.settings")

from DataManager.models import City, Country, Airline
from dataloaders.data_loader import CITY_KEY, COUNTRY_KEY, AIRLINE_KEY


def get_objects(attribute):
    if attribute == CITY_KEY:
        return City.objects
    elif attribute == COUNTRY_KEY:
        return Country.objects
    elif attribute == AIRLINE_KEY:
        return Airline.objects
    return None


def get_column(array, index):
    column = []
    for row in array:
        column.append(row[index])
    return column


def find_key_for_value(dictionary, searched_value):
    for key, value in dictionary.items():
        if value == searched_value:
            return key


def set_plot_settings(title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
