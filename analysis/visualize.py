#!/usr/bin/env python2.7

import re
import os
import csv

import collections

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
#               if csv_file.startswith(scenario) and csv_file.endswith("pdr_aggregated.csv"):
#                   delay_files.append(csv_file)

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

    def _sorted(self, data): 
        convert = lambda text: int(text) if text.isdigit() else text 
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key = alphanum_key)


    def _visualize_pdr(self, directory, pdr_files):
        pdr = {}

        for pdr_file in pdr_files:
            scenario = pdr_file.split("_")[0]
            pdr_file = directory + pdr_file
            result = self._read_csv(pdr_file)
            pdr[scenario] = float(result[1][4])

        xdata = [[]]
        ydata = [[]]

        pattern = re.compile("([a-zA-Z]+)([0-9]+)(([a-zA-Z]+)?)")
        
#        pdr = collections.OrderedDict(self._sorted(pdr.keys()))
        keys = self._sorted(pdr.keys())

        init_algorithm = ""
        init_option = ""
        index = 0
        pause_times = []

        for scenario in keys:
            match = pattern.match(scenario)
            algorithm = match.group(1)
            pause_time = match.group(2)
            option = match.group(3)

            # algorithm has not been set set
            if init_algorithm == "":
                init_algorithm = algorithm
                if init_option == "":
                    init_option = option
            # check if it is already a new scenario
            elif algorithm == init_algorithm:
                if init_option != option:
                   index = index + 1
                   init_option = option
            else:
                init_algorithm = algorithm
                init_option = option
                index = index + 1

            xdata[index].append(pause_time)
            if pause_time not in pause_times:
                pause_times.append(pause_time)
            ydata[index].append(pdr[scenario])
                
        plot = PacketDeliveryRatePlot()
        plot.xlist = xdata
        plot.ylist = ydata
        # FIXME: The tick labes don't match the data points in the graph
        plot.xticklabels = pause_times
        plot.draw(os.path.join(self.csv_location, "avg_packetdeliveryrate.png"))

    
#    def plot_lineplot(self, title, x_label, y_label, x_data, y_data):
#        plot = LinePlot()
#        plot.title = title
#        plot.xlabel = x_label
#        plot.ylabel = y_label
#        plot.draw(x_data, y_data, os.path.join(self.csv_location, "avg_packetdeliveryrate.png"))

