#!/usr/bin/env python2.7

import sys
import numpy as np

from plot.boxplot import BoxPlot

class DelayAnalysis:
    def __init__(self, scenario):
        self.delay = []
        self.scenario = scenario


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
        plot.draw(self.delay, self.scenario + "_delay.png")

        avg_delay = []

        for delay in self.delay:
           avg_delay.append(np.average(delay))

        print "Average Delays per Repetition: ", avg_delay

        # make a plot over all repetitions
        plot = BoxPlot()
        plot.title = "Average Delay"
        plot.xlabel = "Repetition"
        plot.xlabel = "Delay [ms]"
        plot.draw(avg_delay, self.scenario + "_avg_delay.png")
        

	# determine the nodes 
	#print experiment_results.get_average('delay')
#        for node_identifier, results in experiment_results.repetitions[0].get_node_results().iteritems():
#            print results[node_identifier]['delay'];

        
    #    if is_verbose:
    #        self.analyse_single_repetitions(experiment_results)
        
    #    self.check_no_inexplicable_loss(experiment_results)
    #    self.analyse_average_values(experiment_results)
    
