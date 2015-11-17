import json
import re

from Graphs.dataloaders.data_loader import DataLoader

__author__ = 'Magda'


class RubyDataLoader(DataLoader):

    def __init__(self, filename) :
        super().__init__(filename)

    def convert_hash_to_dict(self, ruby_hash):
        # dict_str = ruby_hash.replace(":",'"')    # Remove the ruby object key prefix
        dict_str = ruby_hash
        for i in range(5):
            dict_str = re.sub(self.colon_regexp, '"', dict_str)
        dict_str = dict_str.replace("=>", '" : ')   # swap the k => v notation, and close any unshut quotes
        dict_str = dict_str.replace('""', '"')      # strip back any double quotes we created to sinlges
        print(dict_str)
        return json.loads(dict_str)

    def load(self):
        for filename in self.filenames:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    offer = self.convert_hash_to_dict(line)
                    self.offers_combined.append(offer)
