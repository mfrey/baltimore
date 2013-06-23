#!/usr/bin/env python2.7

import os.path
import sys
import numpy as np

from plot.boxplot import BoxPlot

class DelayAnalysis:
    def __init__(self, scenario, location):
        self.delay = []
        self.scenario = scenario
	self.location = location

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning delay analysis.."
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("delay")
            for node in nodes:
                self.delay.append(experiment_results.get_metric_per_node("delay", node, repetition))

        # make a plot over all repetitions
        plot = BoxPlot()
        plot.title = "Delay per Repetition"
        plot.xlabel = "Repetition"
        plot.xlabel = "Delay [ms]"
        plot.draw(self.delay, os.path.join(self.location, self.scenario + "_delay.png"))

        avg_delay = []

        for delay in self.delay:
           avg_delay.append(np.average(delay))

        print "Average Delays per Repetition: ", avg_delay

        # make a plot over all repetitions
        plot = BoxPlot()
        plot.title = "Average Delay"
        plot.xlabel = "Repetition"
        plot.xlabel = "Delay [ms]"
        plot.draw(avg_delay, os.path.join(self.location, self.scenario + "_avg_delay.png"))
        
