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


class DataLoader:

    def __init__(self, filenames):
        self.offers = []
        self.offers_combined = []
        self.filenames = filenames
        self.colon_regexp = r'(:)(?=(?:[^"]|"[^"]*")*$)'

    def separate_offers(self):
        for offer in self.offers_combined:
            if len(offer[CITY_KEY]) > 0:
                for city in offer[CITY_KEY]:
                    separated_offer = dict()
                    separated_offer[AIRLINE_KEY] = offer[AIRLINE_KEY]
                    separated_offer[TIME_KEY] = offer[TIME_KEY]
                    separated_offer[CITY_KEY] = city
                    separated_offer[PRICE_KEY] = self.parse_prices(offer[PRICE_KEY])

                    # city_obj = City.objects.get(id=city)
                    # print(offer)
                    # if len(offer[AIRLINE_KEY]) > 0:
                    #     print(Airline.objects.get(id=offer[AIRLINE_KEY][0]).name)
                    # print(city_obj.name + " " + city_obj.country.name)

                    self.offers.append(separated_offer)

    def load_country_data(self):
        for offer in self.offers:
            city_id = offer[CITY_KEY]
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