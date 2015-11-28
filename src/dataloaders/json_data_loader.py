import json

from dataloaders.data_loader import DataLoader

__author__ = 'Magda'


class JsonDataLoader(DataLoader):

    def load(self):
        for filename in self.filenames:
            with open(filename, encoding = 'utf-8') as f:
                self.offers += json.load(f)

        self.prepare_data()