#!/usr/bin/env python2.7

import re
import os
import csv
import collections

from plot.lineplot import LinePlot
from plot.packetdeliveryrateplot import PacketDeliveryRatePlot

class Visualize:
    def __init__(self, settings):
        self.csv_location = settings['analysis_location']
	csv_files = []
	pdr_files = []
        self.scenarios = settings['scenarios']

        for file in os.listdir(self.csv_location):
            if file.endswith('csv'):
	        csv_files.append(file.__str__())

        for csv_file in csv_files:
            for scenario in self.scenarios:
               if csv_file.startswith(scenario) and csv_file.endswith("pdr_aggregated.csv"):
                   pdr_files.append(csv_file)

        pdr_files = set(pdr_files)
        self._visualize_pdr(self.csv_location, pdr_files)

#	for csv_file in csv_files:
#            self._read_csv(csv_location + csv_file)

    def _read_csv(self, file_name):
        result = []

        with open(file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	    for row in reader:
                result.append(row)

	result = [row for row in result if len(row) > 1]

        return result


    def _visualize_pdr(self, directory, pdr_files):
        pdr = {}

        for pdr_file in pdr_files:
	    scenario = pdr_file.split("_")[0]
            pdr_file = directory + pdr_file
            result = self._read_csv(pdr_file)
            pdr[scenario] = float(result[1][4])

	xdata = []
        ydata = [[] for scenario in self.scenarios]

        pattern = re.compile("([a-zA-Z]+)([0-9]+)")
        pdr = collections.OrderedDict(sorted(pdr))

	# FIXME: sort the dict beforehand and handle scenarios without numbers in its name
        for index, scenario in enumerate(pdr):
            match = pattern.match(scenario)
            xdata.append(int(match.group(2)))
	    ydata[index].append(pdr[scenario])

        print xdata
        print ydata

        plot = PacketDeliveryRatePlot()
	plot.xlist = xdata
	plot.ylist = ydata
	plot.draw(os.path.join(self.csv_location, "avg_packetdeliveryrate.png"))

    
    def plot_lineplot(self, title, x_label, y_label, x_data, y_data):
        plot = LinePlot()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.draw(x_data, y_data, os.path.join(self.csv_location, "avg_packetdeliveryrate.png"))
	
