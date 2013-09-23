#!/usr/bin/env python2.7

import re
import os
import csv
import math
import random 
import logging
import operator

import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter

from plot.boxplot import BoxPlot
from plot.barchart import BarChart
from plot.lineplot import LinePlot
from plot.packetdeliveryrateplot import PacketDeliveryRatePlot

class Visualize:
    def __init__(self, settings):
        self.csv_location = settings['analysis_location']
        self.logger = logging.getLogger('baltimore.analysis.Visualize')
        
        csv_files = []
        pdr_files = []
        energy_dead_series_files = []
        energy_dead_series_files_raw = []
        path_energy_files = []
        overhead_files = []
        hop_count_files = []

        self.scenarios = settings['scenarios']
        scenario_files = {}

        pdr = {}

        for root, _, files in os.walk(self.csv_location):
            for name in files:
                if name.endswith('csv'):
                   scenario = root.split('/')[-1]
                   if scenario not in scenario_files:
                       scenario_files[scenario] = []
                   scenario_files[scenario].append(os.path.join(root, name))

        for scenario in scenario_files:
            self.logger.debug("scanning files for scenario %s", scenario)
            for csv_file in scenario_files[scenario]:
               if csv_file.endswith("pdr_aggregated.csv"):
                   pdr_files.append(csv_file)
               elif csv_file.endswith("energy-dead-series_raw.csv"):
                   energy_dead_series_files_raw.append(csv_file)
               elif csv_file.endswith("path-energyraw.csv"):
                   path_energy_files.append(csv_file)
               elif csv_file.endswith("energy-dead-series.csv"):
                   energy_dead_series_files.append(csv_file)
#               elif csv_file.endswith("overhead_bit.csv"):
#                   overhead_files.append(csv_file)
               elif csv_file.endswith("overhead_packets.csv"):
                   overhead_files.append(csv_file)
               elif csv_file.endswith("hopCount.csv"):
                   hop_count_files.append(csv_file)
            
            result = self._visualize_pdr(scenario, pdr_files)
            pdr[scenario] = result

#	    self._visualize_eds_raw(scenario, energy_dead_series_files_raw)

#	    self._visualize_eds(scenario, energy_dead_series_files)

#	    self._visualize_path_energy(path_energy_files)

	    self._visualize_hop_count(scenario, hop_count_files)

            pdr_files = []
            energy_dead_series_files = []
            energy_dead_series_files_raw = []
            path_energy_files = []
            hop_count_files = []

        self._generate_overall_pdr(pdr)
        self._generate_overhead(overhead_files)


    def _generate_overhead(self, files):
        self._visualize_overhead(files, "Packet")


    def _generate_overall_pdr(self, pdr):
        plot = PacketDeliveryRatePlot()
        file_name = os.path.join(self.csv_location, "overall_avg_pdr.pdf") 

        for scenario in sorted(pdr.keys()):
            plot.xlist.append(pdr[scenario][0][0])
            plot.ylist.append(pdr[scenario][1][0])
            plot.labels.append(scenario)

        plot.yticks = [60, 70, 80, 90, 92, 94, 96, 100]
        plot.draw(file_name)


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


    def _visualize_hop_count(self, experiment, hop_count_files):
        assert len(hop_count_files) > 0
        hop_count = {}
        max_timestamp_per_scenario = {}
        hop_count_files = self._sorted(hop_count_files)
        bin_size_in_seconds = 10

        for hop_count_file in hop_count_files:
            scenario = hop_count_file.split("/")[-1].split("_")[0]
            result = self._read_csv(hop_count_file)

            result.pop(0)

            max_timestamp_per_scenario[scenario] = np.amax([float(element[2]) for element in result])

            for row in result:
                repetition = row[1]

                if scenario not in hop_count:
                    hop_count[scenario] = {}

                if repetition not in hop_count[scenario]:
                    hop_count[scenario][repetition] = []

                hop_count[scenario][repetition].append(row)

 
        plot = BoxPlot()
        plot.title = "Hop Count"
        plot.ylabel = "Number of Hops"
        plot.xlabel = [[scenario] for scenario in self._sorted(hop_count.keys())]
        data = []

        for scenario in self._sorted(hop_count.keys()):
            scenario_data = []
            for repetition in hop_count[scenario]:
                for entry in hop_count[scenario][repetition]:
                    hops = int(entry[3])
                    scenario_data.append(hops)
            data.append(scenario_data)

        file_name = os.path.join(self.csv_location, experiment +  "-hop_count_boxplot.pdf")
        plot.draw(data, file_name)

        for scenario in self._sorted(hop_count.keys()):
            repetitions = len(hop_count[scenario])
            max_timestamp = max_timestamp_per_scenario[scenario]
            nr_of_bins = int(max_timestamp/bin_size_in_seconds) + 1

            global_bins = {} 

            for repetition in hop_count[scenario]:
                bins_for_this_repetition = {} 

                for row in hop_count[scenario][repetition]:
                    node = row[0]
                    timestamp = float(row[2])
                    value = int(row[3])
                    # get the hop count and add +1 to the corresponding bin
                    # in which interval does the hop count lie?
                    bin_nr = int(math.floor(timestamp/bin_size_in_seconds))
                    
                    if bin_nr not in bins_for_this_repetition:
                        bins_for_this_repetition[bin_nr] = []
                    bins_for_this_repetition[bin_nr].append(value)

                # now save the bins to calculate the average later
                for bin_nr, value in bins_for_this_repetition.iteritems(): 
                    if bin_nr not in global_bins:
                        global_bins[bin_nr] = []
                    global_bins[bin_nr].append(value)

            data = {}

            for bin_nr, value_list in global_bins.iteritems():
                # calculate the average number of dead notes from the corresponding bin of each repetition
                if len(value_list) > 0:
                    average = [np.average([np.average(repetition) for repetition in value_list])]
                else:
                    average = 0

                data[bin_nr] = average

            xdata = []
            ydata = []

            for bin_nr, value in data.iteritems():
                xdata.append(bin_nr * bin_size_in_seconds)
                ydata.append(value)

            ydata = reduce(operator.add, map(lambda x: list(x), [element for element in ydata]))
            file_name = os.path.join(self.csv_location, scenario +  "_hop-count_test.pdf")

            plot = LinePlot()
            plot.title = "Hop Count"
            plot.xlabel = "Time [s]"
            plot.ylabel = "Average Number of Hops"
            plot.xlist.append(xdata)
            plot.ylist.append(ydata)
            plot.xticks = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
            plot.yticks = [1, 5, 10, 15, 20, 25]
            plot.draw(file_name)
 


    def _visualize_eds(self, experiment, eds_files):
        plot = LinePlot()

        eds_files = self._sorted(eds_files)

        self.logger.debug("number of energy dead series files to parse: %d", len(eds_files))

        for eds_file in eds_files:
            scenario = eds_file.split("/")[-1].split("_")[0]
            self.logger.debug("parsing scenario %s and energy dead series file: %s", scenario, eds_file)
            result = self._read_csv(eds_file)

            # remove the row containing the description 
            result.pop(0)

            xlist = []
            ylist = []

            self.logger.debug("number of lines in file %s: %d", eds_file, len(result))

            for row in result:
                timestamp = float(row[0])
                average_number_of_dead_nodes = float(row[1])

                if (len(ylist) - 1) < 0:
                    previous_number_of_dead_nodes = 0
                else:
                    previous_number_of_dead_nodes = ylist[(len(ylist)-1)]

                if average_number_of_dead_nodes != 0 or len(ylist) == 1:
                    xlist.append(timestamp)
                    ylist.append(average_number_of_dead_nodes + previous_number_of_dead_nodes)


            # set the name of the scenario in the plot
            plot.labels.append(scenario)
            # set the values of the x-axis
            plot.xlist.append(xlist)
            # set the values of the y-axis
            plot.ylist.append(ylist)
        
        plot.title = "Energy Dead Series (Average)"
        plot.xlabel = "Time [s]"
        plot.ylabel = "Average Number of Dead Nodes"
        plot.yticks = [0, 5, 10, 20, 30, 40, 50]

        print str(len(xlist)) + " " + str(len(plot.labels))
        print plot.xlist
        print plot.labels

        file_name = os.path.join(self.csv_location, experiment +  "energy_dead_series.pdf")
        plot.draw(file_name)


    def _visualize_eds_raw(self, experiment, eds_files):
        energy_dead_series = {}
        bin_size_in_seconds = 10
        #  max timestamp / bin size in seconds
        nr_of_bins = 0

        max_timestamp_per_scenario = {}
 
        for eds_file in eds_files:
            scenario = eds_file.split("/")[-1].split("_")[0]
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

        plot = BoxPlot()
        plot.title = "Energy Dead Series"
        plot.ylabel = "Time [s]"
        plot.xlabel = [[scenario] for scenario in self._sorted(energy_dead_series.keys())]
        data = []
        # generate box plot        
        for scenario in self._sorted(energy_dead_series.keys()):
            scenario_data = []
            for repetition in energy_dead_series[scenario]:
                for entry in energy_dead_series[scenario][repetition]:
                    timestamp = float(entry[2])
                    scenario_data.append(timestamp)
            data.append(scenario_data)

        file_name = os.path.join(self.csv_location, experiment +  "energy_dead_series_boxplot.pdf")
        plot.draw(data, file_name)

        # generate bar chart        
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
        file_name = os.path.join(self.csv_location, scenario +  "_energy_dead_series.pdf")
        plot.draw(xdata, ydata, file_name)
     

    def _visualize_overhead(self, files, version):
        overhead = {}
        version = version.lower()

        for overhead_file in files:
            scenario = overhead_file.split("/")[-1].split("_")[0]
            result = self._read_csv(overhead_file)
            overhead[scenario] = float(result[1][4])

        keys = self._sorted(overhead.keys())
        data = self._get_keys(keys, overhead)
        keys = self._sorted(data.keys())
        result = self._get_data(data, keys) 

        plot = LinePlot()
        plot.title = "Routing Overhead (" + version + ")"
        plot.xlist = result[0]
        plot.ylist = result[1]
        plot.xlabel = "Pause Time [s]"
        plot.ylabel = version + " %"
        plot.labels = keys 
        plot.yticks = [0, 2, 4, 6]
        plot.legend_location = 4
        file_name = os.path.join(self.csv_location, "overhead_" + version + ".pdf")
        plot.draw(file_name)

    def _visualize_pdr(self, experiment, files):
        """ Plots a line graph of the packet delivery rate of one scenario

        """
        pdr = {}

        for pdr_file in files:
            scenario = pdr_file.split("/")[-1].split("_")[0]
            result = self._read_csv(pdr_file)
            pdr[scenario] = float(result[1][4])

        keys = self._sorted(pdr.keys())
        data = self._get_keys(keys, pdr)
        keys = self._sorted(data.keys())
        result = self._get_data(data, keys) 

        file_name = os.path.join(self.csv_location, experiment + "_avg_packetdeliveryrate.pdf")
        
        plot = PacketDeliveryRatePlot()
        plot.xlist = result[0]
        plot.ylist = result[1]
        plot.labels = keys 
        plot.draw(file_name)

        return (result[0], result[1], keys)


    def _get_data(self, data, keys):
        xdata = []
        ydata = []
        pause_times = []

        for scenario in keys:
            pause_times = sorted(data[scenario].keys())
            xdata.append(pause_times)
            ydata_temp = []

            for pause_time in pause_times:
                ydata_temp.append(data[scenario][pause_time])

            ydata.append(ydata_temp)

        return (xdata, ydata)


    def _get_keys(self, keys, results):
        """ The method returns a dictionary containing scenarios and the corresponding values.
       
        """

        data = {}
        pattern = re.compile("([a-zA-Z]+)([0-9]+)(([a-zA-Z]+)?)")

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

            data[key][pause_time] = results[scenario]

        return data


    def _visualize_path_energy(self, path_energy_files):
        path_energy = {}

        for path_energy_file in path_energy_files:
            scenario = path_energy_file.split("/")[-1].split("_")[0]
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
                plt.ylabel("Energy [mWs]")
                plt.plot(domain, estimate)
                plt.savefig(os.path.join(self.csv_location, file_name + ".pdf"))
                plt.close()

                # prepare data
                number_of_samples = 500
                samples = random.sample(data, number_of_samples)
                timestamp = [float(pair[0]) for pair in samples]
                energy = [float(pair[1]) for pair in samples]

                # plot the path energy with the original data
                figure = plt.figure()
                figure.subplots_adjust(bottom=0.2)
                axis = figure.add_subplot(111)
                plt.plot(domain, estimate)
                plt.plot(timestamp, energy, '.')
                #plt.scatter(timestamp, energy, alpha=0.7)
                plt.title("Path Energy - Node " + str(node) + " (Estimated) for scenario " + scenario)
                plt.xlabel("Time [s]")
                plt.ylabel("Energy [mWs]")
                plt.savefig(os.path.join(self.csv_location, file_name + "_raw.pdf"))
                plt.close()

        # we make a plot for each node (over all scenarios)
        for node in data_all_scenarios:
            plt.title("Path Energy - Node " + str(node) + " (Estimated)")
            plt.xlabel("Time [s]")
            plt.ylabel("Energy [mWs]")
            file_name = "node-" + str(node) + "_path_energy"

            sorted_scenarios = self._sorted(data_all_scenarios[node])

            for scenario in sorted_scenarios:
                domain = data_all_scenarios[node][scenario][0]
                estimate = data_all_scenarios[node][scenario][1]
                plt.plot(domain, estimate, label=scenario)

            plt.legend()
            plt.savefig(os.path.join(self.csv_location, file_name + ".pdf"))
            plt.close()


    def _compute_kernel_regression(self, smoothing_width, data):
        """  Finds a non-linear relation between a pair of random variables X and Y and draws it.

        The method applies a Nadaraya-Watson kernel regression on the given data.

        """
        Tmax = 6000

        # timestamps 
        timestamps = [float(pair[0]) for pair in data]
        # path energy values 
        path_energy = [float(pair[1]) for pair in data]

        bw = smoothing_width

        trange = [0, Tmax]
        bins = 5000

        dx = (trange[1] - trange[0]) / bins

        # compute sum_i K(x - x_i) y_i
        hist_R, edges = np.histogram(timestamps, range=trange, bins=bins, weights=path_energy)
        kernel_density_R = gaussian_filter(hist_R, bw / dx)

        # compute sum_i K(x - x_i)
        hist_T, edges = np.histogram(timestamps, range=trange, bins=bins)
        kernel_density_T = gaussian_filter(hist_T, bw / dx)

        self.logger.debug("kernel density for path energy values is " + str(kernel_density_R))
        self.logger.debug("kernel density for timestamps is " + str(kernel_density_T))

        # compute the Nadaraya-Watson estimate
        interpolated_R = kernel_density_R / kernel_density_T

        # compute the x-axis
        domain = (edges[1:] + edges[:-1]) / 2.0

        return (domain, interpolated_R)


    # TODO
    def _compute_bandwidth(self, data):
        """  Finds a suitable bandwidth for the kernel regression.

        The method ...

        """  
        return .5
