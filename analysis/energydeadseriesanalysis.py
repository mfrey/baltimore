#!/usr/bin/env python2.7

import sys
import numpy as np


from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class EnergyDeadSeriesAnalysis:
    def __init__(self, scenario):
        self.energy_dead_series = {}
        self.scenario = scenario

    def evaluate(self, experiment_results, is_verbose=False):
        repetitions = len(experiment_results.repetitions)
        print "\nRunning energy dead series analysis.."
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("nodeEnergyDepletionTimestamp")
            for node in nodes:
                timestamp = experiment_results.get_metric_per_node("nodeEnergyDepletionTimestamp", node, repetition)

                if self._timestamp_exists(timestamp):
                    self.energy_dead_series[timestamp][repetition] = self.energy_dead_series[timestamp][repetition] + 1
                else:
                    self.energy_dead_series[timestamp] = [] + [0] * repetitions
                    self.energy_dead_series[timestamp][repetition] = 1

        print self.energy_dead_series


    def _timestamp_exists(self, timestamp):
        return self.energy_dead_series.has_key(timestamp)


    def _create_plot(self):
        plot = LinePlot()
        data = []

        for timestamp in sorted(self.energy_dead_series.iterkeys()):       
            plot.xlist.append(timestamp)
            data.append(np.average(self.energy_dead_series[timestamp]))

        plot.title = "Energy Dead Series"
        plot.xlabel = "Time [s]" 
        plot.ylabel = "Dead Nodes" 

        plot.ylist = np.cumsum(data)
        plot.draw(plot.xlist, plot.ylist, "test.png")
#.append(np.avgerage(self.energy_dead_series[timestamp]))


    
