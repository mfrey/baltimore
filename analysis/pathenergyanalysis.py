#!/usr/bin/env python2.7

import sys
import os.path
import numpy as np

from analysis import Analysis

from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class PathEnergyAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "path-energy")
        self.path_energy = {}

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning path energy analysis.."

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("routeEnergy")
            for node in nodes:
                self.path_energy[node] = experiment_results.get_vector_metric_per_node("routeEnergy", node, repetition)

#        print self.path_energy
           

#        self.data = experiment_results.get_average("routeEnergy")
#        print self.data
#        plot = LinePlot()

#        plot.title = "Path Energy (Average)"
#        plot.xlabel = "Time [s]"
#        plot.ylabel = "Energy [J]"
#        plot.draw(self.data, self.data, os.path.join(self.location, self.scenario + "_path_energy.png"))

        

