#!/usr/bin/env python2.7

import logging
import numpy as np

from analysis import Analysis

class DelayAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "delay")

        self.logger = logging.getLogger('baltimore.analysis.DelayAnalysis')
        self.logger.debug('creating an instance of DelayAnalysis for scenario %s', scenario)

        self.data_min = {}
        self.data_max = {}
        self.data_median = {}
        self.data_std = {}
        self.data_avg = {}


    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running delay analysis")

        delay = {} 

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("delay")
            for node in nodes:
                if node not in delay:
                    delay[node] = []
                result = experiment_results.get_metric_per_node("delay", node, repetition)
                delay[node].append(result)

        for node, data  in delay.iteritems():
            self.data_min[node] = [np.amin(repetition) for repetition in data]
            self.data_max[node] = [np.amax(repetition) for repetition in data]
            self.data_median[node] = [np.median(repetition) for repetition in data]
            self.data_std[node] = [np.std(repetition) for repetition in data]
            self.data_avg[node] = [np.average(repetition) for repetition in data]

            self.logger.info("delay [min]: " + "%s  for node %s in scenario %s",
                                 str(self.data_min[node]), node, self.scenario)
            self.logger.info("delay [max]: " + "%s  for node %s in scenario %s",
                                 str(self.data_max[node]), node, self.scenario)
            self.logger.info("delay [median]: " + "%s  for node %s in scenario %s",
                                 str(self.data_median[node]), node, self.scenario)
            self.logger.info("delay [std]: " + "%s  for node %s in scenario %s",
                                 str(self.data_std[node]), node, self.scenario)
            self.logger.info("delay [avg]: " + "%s  for node %s in scenario %s",
                                 str(self.data_avg[node]), node, self.scenario)
                    
        for node, delay in delay.iteritems():
            self.metric = "delay_node-" + str(node)
            # make a plot over all repetitions (per node)
            self.plot_boxplot("Delay per Repetition (Node " + str(node) + ")", "Repetition", "Delay [ms]", delay)

            self.metric = "average_delay_node-" + str(node)
            self.plot_boxplot("Average Delay (Node " + str(node) + ")", "Repetition", "Delay [ms]", self.data_avg[node])
