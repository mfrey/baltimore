#!/usr/bin/env python2.7

import os.path
import sys
import numpy as np

from plot.boxplot import BoxPlot
from analysis import Analysis

class DelayAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "delay")
	# there can be multiple traffic sinks, we store the delay values by means of { node : [] }
        self.delay = {}

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning delay analysis.."
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("delay")
            for node in nodes:
                if node not in self.delay:
                    self.delay[node] = []
                self.delay[node].append(experiment_results.get_metric_per_node("delay", node, repetition))
                      
        for node, delay in self.delay.iteritems():
            self.metric = "delay_node-" + str(node)
            # make a plot over all repetitions (per node)
            self.plot_boxplot("Delay per Repetition (Node " + str(node) + ")", "Repetition", "Delay [ms]", delay)

            average_delay = [np.average(repetition) for repetition in delay]
            print "Average Delays per Repetition (Node " + str(node) + "): ", average_delay
            self.metric = "average_delay_node-" + str(node)
            self.plot_boxplot("Average Delay (Node " + str(node) + ")", "Repetition", "Delay [ms]", average_delay)
