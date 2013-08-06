#!/usr/bin/env python2.7

import re
import os
import csv
import math
import logging

import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter

from plot.packetdeliveryrateplot import PacketDeliveryRatePlot
from plot.barchart import BarChart

class Visualize:
    def __init__(self, settings):
        self.csv_location = settings['analysis_location']
        self.logger = logging.getLogger('baltimore.analysis.Visualize')
        
        csv_files = []
        pdr_files = []
        energy_dead_series_files = []
        path_energy_files = []

        self.scenarios = settings['scenarios']

        for file in os.listdir(self.csv_location):
            if file.endswith('csv'):
	        csv_files.append(file.__str__())

        for csv_file in csv_files:
            for scenario in self.scenarios:
               if csv_file.startswith(scenario) and csv_file.endswith("pdr_aggregated.csv"):
                   pdr_files.append(csv_file)
               elif csv_file.startswith(scenario) and csv_file.endswith("energy-dead-series_raw.csv"):
                   energy_dead_series_files.append(csv_file)
               elif csv_file.startswith(scenario) and csv_file.endswith("path-energyraw.csv"):
                   path_energy_files.append(csv_file)

        pdr_files = set(pdr_files)
        self._visualize_pdr(self.csv_location, pdr_files)

        energy_dead_series_files = set(energy_dead_series_files)
        self._visualize_eds(self.csv_location, energy_dead_series_files)

        path_energy_files = set(path_energy_files)
        self._visualize_path_energy(self.csv_location, path_energy_files)


    def _read_csv(self, file_name):
        result = []

        with open(file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                result.append(row)

        return [row for row in result if len(row) > 1]


    def _sorted(self, data): 
        convert = lambda text: int(text) if text.isdigit() else text 
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key = alphanum_key)


    def _visualize_eds(self, directory, eds_files):
        #
        energy_dead_series = {}
        #
        bin_size_in_seconds = 10
        #  max timestamp / bin size in seconds
        nr_of_bins = 0

        max_timestamp_per_scenario = {}

        for eds_file in eds_files:
            scenario = eds_file.split("_")[0]
            eds_file = directory + eds_file
            result = self._read_csv(eds_file)

            # remove the row containing the description 
            result.pop(0)

            max_timestamp_per_scenario[scenario] = np.amax([float(element[2]) for element in result])

            for row in result:
                repetition = row[0]

                if scenario not in energy_dead_series:
                    energy_dead_series[scenario] = {}

                if repetition not in energy_dead_series[scenario]:
                    energy_dead_series[scenario][repetition] = []

                energy_dead_series[scenario][repetition].append(row)

        
        for scenario in energy_dead_series:
            repetitions = len(energy_dead_series[scenario])
            max_timestamp = max_timestamp_per_scenario[scenario]
            nr_of_bins = int(max_timestamp/bin_size_in_seconds) + 1
            
            self.logger.debug("number of bins: %d (for scenario %s)", nr_of_bins, scenario)

            # create all bins and initialize with zero and each bin is a list of dead notes per repetition 
            global_bins = { key : [] for key in range(0, nr_of_bins) } 

            for repetition in energy_dead_series[scenario]:
                bins_for_this_repetition = { key : 0 for key in range(0, nr_of_bins) } 

                for row in energy_dead_series[scenario][repetition]:
                    node = row[1]
                    timestamp = float(row[2])
                    # get the timestamp and add +1 to the corresponding bin
                    # in which interval does the timestamp lie?
                    bin_nr = int(math.floor(timestamp/bin_size_in_seconds))
                    bins_for_this_repetition[bin_nr] += 1

                # now save the bins to calculate the average later
                for bin_nr, value in bins_for_this_repetition.iteritems(): 
                    global_bins[bin_nr].append(value)

            eds = {}

            for bin_nr, value_list in global_bins.iteritems():
                # calculate the average number of dead notes from the corresponding bin of each repetition
                if value_list:
                    average = np.average(value_list)
                else:
                    average = 0

                eds[bin_nr] = average

            self._plot_energy_dead_series(scenario, eds, bin_size_in_seconds)
            # reset the global bin
            global_bins = { key : [] for key in range(0, nr_of_bins-1) } 
        

    def _plot_energy_dead_series(self, scenario, energy_dead_series, bin_size_in_seconds):
        xdata = []
        ydata = []

        for bin_nr, value in energy_dead_series.iteritems():
            xdata.append(bin_nr * bin_size_in_seconds)
            ydata.append(value)
 
        ydata = np.cumsum(ydata)

        plot = BarChart()
        plot.title = "Energy Dead Series"
        plot.xlabel = "Time [s]"
        plot.ylabel = "Dead Nodes"
        plot.bar_widths = -1
        plot.draw(xdata, ydata, os.path.join(self.csv_location, scenario + "_energy-dead-series.png"))
     


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
        keys = self._sorted(pdr.keys())

        init_algorithm = ""
        init_option = ""
        index = 0
        pause_times = []
        scenarios = []

        self.logger.debug("sorted keys " + str(keys)) 

        data = {}

        # build up a temporary data structure holding scenario/pause times/pdrs
        for scenario in keys:
            match = pattern.match(scenario)
            algorithm = match.group(1)
            pause_time = int(match.group(2))
            option = match.group(3)

            self.logger.debug("parsing data for algorithm %s, pause time %s and option %s", algorithm, pause_time, option)
            key = algorithm + option 

            if key not in data:
               data[key] = {}
            
            if pause_time not in data[key]:
               data[key][pause_time] = 0

            data[key][pause_time] = pdr[scenario]

            if key not in scenarios:
                scenarios.append(key)

        keys = self._sorted(data.keys())
        xdata = []
        ydata = []


        for scenario in keys:
            pause_times = sorted(data[scenario].keys())
            xdata.append(pause_times)
            ydata_temp = []

            for pause_time in pause_times:
                ydata_temp.append(data[scenario][pause_time])

            ydata.append(ydata_temp)
                
        plot = PacketDeliveryRatePlot()
        plot.xlist = xdata
        plot.ylist = ydata
        # FIXME: The tick labes don't match the data points in the graph
        plot.xticklabels = pause_times
        # better check that
        plot.labels = keys
        plot.draw(os.path.join(self.csv_location, "avg_packetdeliveryrate.png"))


    def _visualize_path_energy(self, directory, path_energy_files):
        path_energy = {}

        for path_energy_file in path_energy_files:
            scenario = path_energy_file.split("_")[0]
            path_energy_file = directory + path_energy_file
            result = self._read_csv(path_energy_file)

            # removes the header of the csv file
            result.pop(0)

            for entry in result:
                repetition = int(entry[0])
                node = entry[1]
                timestamp = float(entry[2])
                energy = float(entry[3])

                if scenario not in path_energy:
                    path_energy[scenario] = {}

                if node not in path_energy[scenario]:
                    path_energy[scenario][node] = []
 
                # the entry follows the format: timestamp, path energy
                path_energy[scenario][node].append((timestamp, energy))

        # we store the result for all scenarios, so we can generate a overall plot
        data_all_scenarios = {}

        for scenario in path_energy:
            for node in path_energy[scenario]:
                data = path_energy[scenario][node]
                # apply kernel regression
                result = self._compute_kernel_regression(0.5, data)
                domain = result[0]
                estimate = result[1]

                if node not in data_all_scenarios:
                    data_all_scenarios[node] = {}

                if scenario not in data_all_scenarios[node]:
                    data_all_scenarios[node][scenario] = None

                data_all_scenarios[node][scenario] = result
                # build up file name
                file_name = scenario + "_node-" + str(node) + "path_energy"

                # plot the path energy
                plt.title("Path Energy - Node " + str(node) + " (Estimated) for scenario " + scenario)
                plt.xlabel("Time [s]")
                plt.ylabel("Energy [J]")
                plt.plot(domain, estimate)
                plt.savefig(os.path.join(self.csv_location, file_name + ".png"))
                plt.close()

        # we make a plot for each node (over all scenarios)
        for node in data_all_scenarios:
            plt.title("Path Energy - Node " + str(node) + " (Estimated)")
            plt.xlabel("Time [s]")
            plt.ylabel("Energy [J]")
            file_name = "node-2" + str(node) + "_path_energy"

            for scenario in data_all_scenarios[node]:
                domain = data_all_scenarios[node][scenario][0]
                estimate = data_all_scenarios[node][scenario][1]
                plt.plot(domain, estimate, label=scenario)

            plt.legend()

            plt.savefig(os.path.join(self.csv_location, file_name + ".png"))
            plt.close()


    def _compute_kernel_regression(self, smoothing_width, data):
        """  Finds a non-linear relation between a pair of random variables X and Y and draws it.

        The method applies a Nadaraya-Watson kernel regression on the given data.

        """
        Tmax = 6000

        T = [float(pair[0]) for pair in data]
        R = [float(pair[1]) for pair in data]
        bw = smoothing_width

        trange = [0, Tmax]
        bins = 5000

        dx = (trange[1] - trange[0]) / bins

        # compute sum_i K(x - x_i) y_i
        hist_R, edges = np.histogram(T, range=trange, bins=bins, weights=R)
        kde_R = gaussian_filter(hist_R, bw / dx)

        # compute sum_i K(x - x_i)
        hist_T, edges = np.histogram(T, range=trange, bins=bins)
        kde_T = gaussian_filter(hist_T, bw / dx)

        self.logger.debug("kde_R is " + str(kde_R))
        self.logger.debug("kde_T is " + str(kde_R))

        # compute the Nadaraya-Watson estimate
        interpolated_R = kde_R / kde_T

        # compute the x-axis
        domain = (edges[1:] + edges[:-1]) / 2.0

        return (domain, interpolated_R)

