# -*- coding: utf-8 -*-
from datetime import time, datetime
from math import floor
from matplotlib import pyplot as plt
import numpy as np

__author__ = 'Magda'


def get_time_obj(minutes_total):
    hour = floor(minutes_total / 60)
    if hour == 24:
        hour = 0
    minute = minutes_total % 60
    time_obj = time(hour = hour, minute= minute)
    return time_obj


def get_num_from_time(time_obj):
    return time_obj.hour * 60 + time_obj.minute


def get_time_labels(number_of_labels=48, span=30) :
    """
    Generates labels for time histogram.
    :param number_of_labels: Number of labels to generate
    :param span: Number of minutes between consecutive labels
    :return: An array of strings in form 'HH:mm'
    """

    minutes_total = 0
    times = []
    for i in range(number_of_labels + 1):
        if minutes_total == 24 * 60:
            minutes_total = 0
        time_obj = get_time_obj(minutes_total)
        times.append(time_obj.strftime("%H:%M"))
        minutes_total += span

    return times

def make_time_histogram(times, minute_span):
    number_of_bins = int(floor(24 * 60 / minute_span))
    times_mapped = [ datetime.strptime(x, "%H:%M") for x in times ]
    times_mapped = [ get_num_from_time(x) for x in times_mapped ]
    # times_mapped = date2num(times_mapped)
    # print(times_mapped)
    # print(list(filter(lambda x: x < 60, times_mapped)))

    time_labels = get_time_labels(number_of_bins, minute_span)

    fig, ax = plt.subplots()
    counts, bins, patches = plt.hist(times_mapped, range=[0, 60 * 24], bins=number_of_bins)

    ax.set_xticks(bins)
    ax.set_xticklabels(time_labels,rotation=45, rotation_mode="anchor", ha="right")

    # Label the raw counts and the percentages below the x-axis...
    bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    for count, x in zip(counts, bin_centers):
        # Label the raw counts
        ax.annotate(str(int(count)), xy=(x, 0), xycoords=('data', 'axes fraction'),
            xytext=(0, -50), textcoords='offset points', va='top', ha='center')

        # Label the percentages
        percent = '%0.0f%%' % (100 * float(count) / counts.sum())
        ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
            xytext=(0, -75), textcoords='offset points', va='top', ha='center')


    # Give ourselves some more room at the bottom of the plot
    plt.subplots_adjust(left=0.05, bottom=0.25)

    plt.title('Histogram of times when offers were posted on Fly4Free')
    plt.ylabel('Number of occurrences')
    # plt.xlabel('Time of day')

    plt.show()