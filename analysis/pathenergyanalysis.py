#!/usr/bin/env python2.7

import sys
import os.path
import numpy as np

from collection import OrderedDict

from analysis import Analysis
from analysis import PathEnergy

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
                timestamp = data[0] 
                path_energy = data[1]

                if node not in self.path_energy.keys():
                    # we store the timestamp/path_energy in a dict { float:[timestamp] } fashion
                    self.path_energy[node] = {}

                if timestamp not in self.path_energy[node].keys():
                    self.path_energy[node][timestamp] = [-1] * repetitions

                self.path_energy[node][timestamp][repetition] = path_energy

        for node in sorted(self.path_energy.iterkeys()):       
            xdata = []
            ydata = []
            for timestamp in sorted(self.path_energy[node].iterkeys()):       
                xdata.append(timestamp)
                ydata.append(self.path_energy[node][timestamp])
#                ydata.append(np.average(self.path_energy[node][timestamp]))
           
	    path_energy = PathEnergy(node, xdata, ydata)
	    self.path_energy_temp[node] = path_energy
#            self._fill_missing_data(xdata, ydata)

#            self.metric = "path-energy_node-" + str(node)
#            self.plot_lineplot("Path Energy (Average, Node " + str(node) + ")", "Time [s]", "Energy [J]", xdata, ydata)
        
#    def sort(self):
#        for node in self.path_energy:
#            ordered_timestamps = OrderedDict(sorted(self.path_energy[node].items(), key=lambda t: t[1]))
#            for timestamp in sorted(self.path_energy[node]): 
