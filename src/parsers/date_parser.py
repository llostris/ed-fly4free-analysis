# -*- coding: utf-8 -*-

import datetime


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