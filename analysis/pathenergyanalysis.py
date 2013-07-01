#!/usr/bin/env python2.7

import sys
import os.path
import numpy as np
import traceback

import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

from collections import OrderedDict

from analysis import Analysis
from pathenergy import PathEnergy

from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class PathEnergyAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "path-energy")
        self.path_energy = {}
        self.path_energy_temp = {}

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning path energy analysis.."

        repetitions = experiment_results.get_number_of_repetitions()

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("routeEnergy")
            for node in nodes:
                data = experiment_results.get_tuple_metric_per_node("routeEnergy", node, repetition)

                for pair in data:
                    timestamp = float(pair[0])
                    path_energy = float(pair[1])

                    if node not in self.path_energy.keys():
                        # we store the timestamp/path_energy in a dict { float:[timestamp] } fashion
                        self.path_energy[node] = {}

                    if timestamp not in self.path_energy[node].keys():
                        #self.path_energy[node][timestamp] = [-1] * repetitions
                        self.path_energy[node][timestamp] = [0] * repetitions

                    self.path_energy[node][timestamp][repetition] = path_energy

        for node in sorted(self.path_energy.iterkeys()):       
            xdata = []
            ydata = []

            for timestamp in sorted(self.path_energy[node]):       
                xdata.append(timestamp)
#                ydata.append(self.path_energy[node][timestamp])
                ydata.append(np.average(self.path_energy[node][timestamp]))

#            path_energy = PathEnergy(node, xdata, ydata)
#            self.path_energy_temp[node] = path_energy
#            self._fill_missing_data(xdata, ydata)

            self.metric = "path-energy_node-" + str(node)
            self.plot_lineplot("Path Energy (Average, Node " + str(node) + ")", "Time [s]", "Energy [J]", xdata, ydata)
 
        try:
           self.sort(self.path_energy_temp, experiment_results.get_number_of_repetitions())
           for node in self.path_energy_temp:
               for timestamp in self.path_energy_temp[node]:
                   print node, " - ", timestamp, " <> ", self.path_energy_temp[node].energy[self.path_energy_temp[node].get_index_timestamp(timestamp)]
        except:
           print '-'*60
           traceback.print_exc(file=sys.stdout)
           print '-'*60
        
    def sort(self, data, repetitions):
        # iterate over all nodes
        for node in data:
            # iterate over all repetitions
            for repetition in range(0, repetitions):
                # for each timestamp
                for timestamp in data[node]:
                    index = data[node].get_index_timestamp(timestamp)
                    # check if the current energy value is not set 
                    if data[node].energy[index][repetition] == -1:
                        # we are not at the last timestamp
                        if index != data[node].size():
                            for future in data[node].timestamp[index:]:
                                if data[node].energy[data[node].get_index_timestamp(future)][repetition] != -1:
                                    data[node].energy[index][repetition] = data[node].energy[data[node].get_index_timestamp(future)][repetition]
                                    break
                        # we are at the last timestamp and have to go the list backwards
                        else:
                            for past in reversed(data[node]):
                                if data[node].energy[data[node].get_index_timestamp(future)][repetition] != -1:
                                    data[node].energy[index][repetition] = data[node].energy[data[node].get_index_timestamp(past)][repetition]
                                    break


    def evaluate_different(self, experiment_results):
        Tmax = 6000
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("routeEnergy")
            for node in nodes:
                data = experiment_results.get_tuple_metric_per_node("routeEnergy", node, repetition)

                T = [float(pair[0]) for pair in data]
                R = [float(pair[1]) for pair in data]
#                bw = smoothing_width
                bw = 0.5

                trange = [0, Tmax]
                bins = 5000

                dx = (trange[1] - trange[0]) / bins

                # compute sum_i K(x - x_i) y_i
                hist_R, edges = np.histogram(T, range=trange, bins=bins, weights=R)
                kde_R = gaussian_filter(hist_R, bw / dx)

                # compute sum_i K(x - x_i)
                hist_T, edges = np.histogram(T, range=trange, bins=bins)
                kde_T = gaussian_filter(hist_T, bw / dx)

                # compute the Nadaraya-Watson estimate
                interpolated_R = kde_R / kde_T

                # computer x-axis
                domain = (edges[1:] + edges[:-1]) / 2.0

                plt.plot(domain, interpolated_R)
                file_name = "alternative_path-energy_node-" + str(node)
                plt.savefig(os.path.join(self.location, self.scenario + "_" + file_name + ".png"))
                plt.close()
