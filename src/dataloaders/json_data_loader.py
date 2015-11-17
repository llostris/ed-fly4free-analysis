import json

from dataloaders.data_loader import DataLoader

__author__ = 'Magda'


class JsonDataLoader(DataLoader):

    def load(self):
        for filename in self.filenames:
            with open(filename) as f:
                self.offers_combined += json.load(f)
