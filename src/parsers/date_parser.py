# -*- coding: utf-8 -*-

import datetime

class Season:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end


class DateParser:

    def __init__(self):
        self.months = {
            'stycznia' : 1,
            'lutego' : 2,
            'marca' : 3,
            'kwietnia' : 4,
            'maja' : 5,
            'czerwca' : 6,
            'lipca' : 7,
            'sierpnia' : 8,
            'września' : 9,
            'października' : 10,
            'listopada' : 11,
            'grudnia' : 12
        }
        self.seasons = {
            'winter' : [ 1, 2, 3 ],
            'spring' : [ 4, 5, 6 ],
            'summer' : [ 7, 8, 9 ],
            'autumn' : [ 10, 11, 12]
        }
        # self.season_dates = {
        #     'summer' : Season('summer', datetime.date(month=6, day=23)),
        #     'autumn' : Season('autumn', datetime.date(month=9, day = 23)),
        # }


    def parse_date(self, date_str):
        splitted = date_str.split()
        day = int(splitted[0])
        month = self.months[splitted[1]]
        year = int(splitted[2])
        return datetime.date(year, month, day)

    @staticmethod
    def get_month_label(offers_by_month):
        labels = dict()
        for month in offers_by_month:
            labels[month] = datetime.date(month=month, day = 1, year = 2015).strftime('%B')
        return labels

    @staticmethod
    def get_month_labels_for_plot(offers_by_month):
        labels = []
        for month in offers_by_month:
            labels.append((month, datetime.date(month=month, day = 1, year = 2015).strftime('%B')))
        return labels