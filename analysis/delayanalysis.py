#!/usr/bin/env python2.7

import numpy as np

from analysis import Analysis

class DelayAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "delay")
        self.data_min = {}
        self.data_max = {}
        self.data_median = {}
        self.data_std = {}
        self.data_avg = {}


    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning delay analysis.."

        delay = {} 

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("delay")
            for node in nodes:
                if node not in delay:
                    delay[node] = []
                result = experiment_results.get_metric_per_node("delay", node, repetition)
                delay[node].append(result)

                self.data_min[node] = np.amin(result)
                self.data_max[node] = np.amax(result)
                self.data_median[node] = np.median(result)
                self.data_std[node] = np.std(result)
                self.data_avg[node] = np.average(result)
                    
        for node, delay in delay.iteritems():
            self.metric = "delay_node-" + str(node)
            # make a plot over all repetitions (per node)
            self.plot_boxplot("Delay per Repetition (Node " + str(node) + ")", "Repetition", "Delay [ms]", delay)

            average_delay = [np.average(repetition) for repetition in delay]
            # better check
            self.data_avg = average_delay
            print "Average Delays per Repetition (Node " + str(node) + "): ", average_delay
            self.metric = "average_delay_node-" + str(node)
            self.plot_boxplot("Average Delay (Node " + str(node) + ")", "Repetition", "Delay [ms]", average_delay)
