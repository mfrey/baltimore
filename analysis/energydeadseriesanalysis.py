#!/usr/bin/env python2.7

import sys
import numpy as np

from analysis import Analysis

from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class EnergyDeadSeriesAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "energy-dead-series")
        self.energy_dead_series = {}

    def evaluate(self, experiment_results, is_verbose=False):
        repetitions = len(experiment_results.repetitions)
        print "\nRunning energy dead series analysis.."
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("nodeEnergyDepletionTimestamp")
            for node in nodes:
                #timestamp = experiment_results.get_metric_per_node("nodeEnergyDepletionTimestamp", node, repetition)
                # FIXME
                timestamp = experiment_results.repetitions[repetition].get_node_results()[node]["nodeEnergyDepletionTimestamp"]

                if self._timestamp_exists(timestamp):
                    self.energy_dead_series[timestamp][repetition] = self.energy_dead_series[timestamp][repetition] + 1
                else:
                    self.energy_dead_series[timestamp] = [] + [0] * repetitions
                    self.energy_dead_series[timestamp][repetition] = 1

        print self.energy_dead_series

        self._create_boxplot()

    def _create_boxplot(self):
        xdata = []
        ydata = []
     
        for timestamp in sorted(self.energy_dead_series.iterkeys()):       
            xdata.append(timestamp)
            ydata.append(np.average(self.energy_dead_series[timestamp]))
 
        ydata = np.cumsum(ydata)
        self.plot_lineplot("Energy Dead Series", "Time [s]", "Dead Nodes", xdata, ydata)


    def _timestamp_exists(self, timestamp):
        return self.energy_dead_series.has_key(timestamp)


    
