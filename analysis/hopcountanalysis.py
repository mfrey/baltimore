#!/usr/bin/env python2.7

import logging
import numpy as np

from analysis import Analysis

class HopCountAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "hopCount", repetitions, csv)

        self.logger = logging.getLogger('baltimore.analysis.HopCountAnalysis')
        self.logger.debug('creating an instance of HopCountAnalysis for scenario %s', scenario)

        self.data_min = {}
        self.data_max = {}
        self.data_median = {}
        self.data_std = {}
        self.data_avg = {}


    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running hop count analysis")

        hop_count = {} 

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("hopCount", repetition)
            for node in nodes:
                if node not in hop_count:
                    hop_count[node] = []
                result = experiment_results.get_metric_per_node("hopCount", node, repetition)
                hop_count[node].append(result)

        for node, data  in hop_count.iteritems():
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

            self.logger.info("Printing average hop count statistics for node %s", node)
            self.logger.info("Minimum hop count = %f seconds", avg_minimum)
            self.logger.info("Maximum hop count = %f seconds", avg_maximum)
            self.logger.info("Std.Deviation     = %f seconds", avg_stdDev)
            self.logger.info("Average hop count = %f seconds", avg_average)
            self.logger.info("Median hop count  = %f seconds", avg_median)
        if self.draw:            
            for node in hop_count:
                self.metric = "hop_count_node-" + str(node)
                self.plot_boxplot("Average Hop Count (Node " + str(node) + ")", "Repetition", "Hop Count [ms]", self.data_avg[node])

        if self.csv:
            self.export_csv()
            self.export_csv_raw(delay)

    def export_csv(self):
        self.metric = "hopCount"
        file_name = self.scenario + "_" + self.metric + "_aggregated.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - hop count for scenario ' + self.scenario],['# aggregated over ' + str(self.repetitions) + ' repetitions'],['#']]
        header = ['node', 'min', 'max', 'median', 'std', 'avg']

        data = []

        # this assumes that if self.data_min is set, that also the other metrics are set (avg, median, std, ...)
        for node in self.data_min:
            data.append([node, self.data_min[node], self.data_max[node], self.data_median[node], self.data_std[node],  self.data_avg[node]])

        self._write_csv_file(file_name, disclaimer, header, data)

    def export_csv_raw(self, raw_data):
        self.metric = "hopCount"
        file_name = self.scenario + "_" + self.metric + ".csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - hop count for scenario ' + self.scenario],['#']]
        header = ['node', 'repetition', 'hop count']

        data = []

        # this assumes that if self.data_min is set, that also the other metrics are set (avg, median, std, ...)
        for node, hop_counts in raw_data.iteritems():
            for repetition, values in enumerate(hop_counts):
                for element in values:
	                data.append([node, repetition, element])
              
        self._write_csv_file(file_name, disclaimer, header, data)
