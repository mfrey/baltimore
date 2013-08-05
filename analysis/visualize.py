#!/usr/bin/env python2.7

import re
import os
import csv
import logging

import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter

from plot.packetdeliveryrateplot import PacketDeliveryRatePlot

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
               elif csv_file.startswith(scenario) and csv_file.endswith("energy-dead-series.csv"):
                   energy_dead_series_files.append(csv_file)
               elif csv_file.startswith(scenario) and csv_file.endswith("path-energyraw.csv"):
                   path_energy_files.append(csv_file)
               else:
                   self.logger.debug("file not supported (yet) " + csv_file)

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
        eds = {}


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
                file_name = scenario + "_node_" + str(node) + "path_energy"

                # plot the path energy
                plt.title("Path Energy - Node " + str(node) + " (Estimated)")
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
            file_name = "node_" + str(node) + "path_energy"

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


