import os

# load Django settings - must be done before loading any Django objects!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Fly4FreeExplorer.settings")

from DataManager.models import City, Airline

__author__ = 'Magda'


CITY_KEY = "cities"
AIRLINE_KEY = "airlines"
TIME_KEY = "time"
COUNTRY_KEY = "country"
PRICE_KEY = "prices"
SOURCES_KEY = "sources"
DESTINATION_KEY = "destinations"


class DataLoader:

    def __init__(self, filenames):
        self.offers = []
        self.offers_by_destination = []
        self.offers_by_source = []
        self.filenames = filenames
        self.colon_regexp = r'(:)(?=(?:[^"]|"[^"]*")*$)'

    def separate_offers(self, property=DESTINATION_KEY):
        separated_offers = []

        for offer in self.offers:
            if len(offer[property]) > 0:
                for city in offer[property]:
                    separated_offer = dict()
                    separated_offer[AIRLINE_KEY] = offer[AIRLINE_KEY]
                    separated_offer[TIME_KEY] = offer[TIME_KEY]
                    separated_offer[PRICE_KEY] = offer[PRICE_KEY]
                    separated_offer[property] = city
                    separated_offer[CITY_KEY] = city
                    if property == DESTINATION_KEY:
                        separated_offer[SOURCES_KEY] = offer[SOURCES_KEY]
                    else:
                        separated_offer[DESTINATION_KEY] = offer[DESTINATION_KEY]

                    separated_offers.append(separated_offer)

        if property == DESTINATION_KEY:
            self.offers_by_destination = separated_offers
        else:
            self.offers_by_source = separated_offers

    def load_country_data(self):
        properties = [ SOURCES_KEY, DESTINATION_KEY ]

        for offer in self.offers_by_destination:
            city_id = offer[DESTINATION_KEY]
            city = City.objects.get(id=city_id)
            offer[COUNTRY_KEY] = city.country.id

        for offer in self.offers_by_source:
            city_id = offer[SOURCES_KEY]
            city = City.objects.get(id=city_id)
            offer[COUNTRY_KEY] = city.country.id


    def load_labels(self):
        pass

    @staticmethod
    def parse_prices(price_list):
        parsed = []
        for price in price_list:
            price_int = int(price.replace(' PLN', ''))
            parsed.append(price_int)
        return parsed

    def prepare_data(self):
        for offer in self.offers:
            offer[PRICE_KEY] = self.parse_prices(offer[PRICE_KEY])