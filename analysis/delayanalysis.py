#!/usr/bin/env python3

import logging
import numpy as np

from .analysis import Analysis

class DelayAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "delay", repetitions, csv)

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
            nodes = experiment_results.nodes_have_metric("delay", repetition)
            for node in nodes:
                if node not in delay:
                    delay[node] = []
                result = experiment_results.get_metric_per_node("delay", node, repetition)
                delay[node].append(result)

        for node, data  in list(delay.items()):
            self.data_min[node] = [np.amin(repetition) for repetition in data]
            self.data_max[node] = [np.amax(repetition) for repetition in data]
            self.data_median[node] = [np.median(repetition) for repetition in data]
            self.data_std[node] = [np.std(repetition) for repetition in data]
            self.data_avg[node] = [np.average(repetition) for repetition in data]

            avg_minimum = np.average(self.data_min[node])
            avg_maximum = np.average(self.data_max[node])
            avg_median = np.average(self.data_median[node])
            avg_stdDev = np.average(self.data_std[node])
            avg_average = np.average(self.data_avg[node])

            self.logger.info("Printing average delay statistics for node %s", node)
            self.logger.info("Minimum delay = %f seconds", avg_minimum)
            self.logger.info("Maximum delay = %f seconds", avg_maximum)
            self.logger.info("Std.Deviation = %f seconds", avg_stdDev)
            self.logger.info("Average delay = %f seconds", avg_average)
            self.logger.info("Median delay  = %f seconds", avg_median)
        if self.draw:            
            for node in delay:
                self.metric = "delay_node-" + str(node)
            # make a plot over all repetitions (per node)
  #          self.plot_boxplot("Delay per Repetition (Node " + str(node) + ")", "Repetition", "Delay [ms]", delay)

   #         average_delay = [np.average(repetition) for repetition in delay]
   #         print "Average Delays per Repetition (Node " + str(node) + "): ", average_delay
   #         self.metric = "average_delay_node-" + str(node)
   #         self.plot_boxplot("Average Delay (Node " + str(node) + ")", "Repetition", "Delay [ms]", average_delay)
                self.metric = "average_delay_node-" + str(node)
                self.plot_boxplot("Average Delay (Node " + str(node) + ")", "Repetition", "Delay [ms]", self.data_avg[node])

        if self.csv:
            self.export_csv()
            self.export_csv_raw(delay)

    def export_csv(self):
        self.metric = "delay"
        file_name = self.scenario + "_" + self.metric + "_aggregated.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - delay for scenario ' + self.scenario],['# aggregated over ' + str(self.repetitions) + ' repetitions'],['#']]
        header = ['node', 'min', 'max', 'median', 'std', 'avg']

        data = []

        # this assumes that if self.data_min is set, that also the other metrics are set (avg, median, std, ...)
        for node in self.data_min:
            data.append([node, self.data_min[node], self.data_max[node], self.data_median[node], self.data_std[node],  self.data_avg[node]])

        self._write_csv_file(file_name, disclaimer, header, data)

    def export_csv_raw(self, raw_data):
        self.metric = "delay"
        file_name = self.scenario + "_" + self.metric + ".csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - delay for scenario ' + self.scenario],['#']]
        header = ['node', 'repetition', 'delay']

        data = []

        # this assumes that if self.data_min is set, that also the other metrics are set (avg, median, std, ...)
        for node, delays  in list(raw_data.items()):
            for repetition, values in enumerate(delays):
                for element in values:
	                data.append([node, repetition, element])
              
        self._write_csv_file(file_name, disclaimer, header, data)
