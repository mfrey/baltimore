#!/usr/bin/env python3

import csv
import os.path
import logging
import datetime

from plot.boxplot import BoxPlot
from plot.lineplot import LinePlot
from plot.barchart import BarChart

class Analysis:
    def __init__(self, scenario, location, metric, repetitions, csv):
        self.scenario = scenario
        self.location = location
        self.metric = metric
        self.logger = logging.getLogger('baltimore.analysis.Analysis')
        self.date = datetime.datetime.now()
        self.repetitions = repetitions
        self.csv = csv
        self.draw = False

    def plot_lineplot(self, title, x_label, y_label, x_data, y_data):
        plot = LinePlot()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.draw(x_data, y_data, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))

    def plot_boxplot(self, title, x_label, y_label, data):
        plot = BoxPlot()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.draw(data, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))

    def plot_barchart(self, title, x_label, y_label, x_data, y_data, bar_widths=-1):
        plot = BarChart()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.bar_widths = bar_widths
        plot.draw(x_data, y_data, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))

    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)

    def print_analysis_header(self, results):
        nr_of_repetitions = results.get_number_of_repetitions()
        print(("Overall statistics (averaged over %d iterations)" % nr_of_repetitions))
        print(('=' * 100))
        print((" " * 42 + "#   Average    Median   Std.Dev       Min       Max"))
        print(('-' * 100))

    def _get_percent_string(self, value, nr_of_packets):
        if nr_of_packets > 0:
            return "%6.2f%%" % ((value/float(nr_of_packets)) * 100.0)
        else:
            return "  0.00%%"

    def _write_csv_file(self, file_name, disclaimer, header, data):
        with open(os.path.join(self.location, file_name), "wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for line in disclaimer:
                writer.writerow(line)

            writer.writerow(header)

            for line in data:
                writer.writerow(line)
