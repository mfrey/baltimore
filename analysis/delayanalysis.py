#!/usr/bin/env python2.7

import os.path
import sys
import numpy as np

from plot.boxplot import BoxPlot
from analysis import Analysis

class DelayAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "delay")
        self.delay = []

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning delay analysis.."
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("delay")
            for node in nodes:
                self.delay.append(experiment_results.get_metric_per_node("delay", node, repetition))

        # make a plot over all repetitions
        self.plot_boxplot("Delay per Repetition", "Repetition", "Delay [ms]", self.delay)

        average_delay = [np.average(delay) for delay in self.delay]
        print "Average Delays per Repetition: ", average_delay
        # rename metric for box plot (otherwise the previous plot would get overriden)
        self.metric = "avg_delay"
        # make a plot over all repetitions
        self.plot_boxplot("Average Delay", "Repetition", "Delay [ms]", average_delay)
