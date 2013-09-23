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
        raw_data = []

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("hopCount", repetition)

            for node in nodes:
                data = experiment_results.get_tuple_metric_per_node("hopCount", node, repetition)

                for element in data:
                    raw_data.append([repetition, node, float(element[0]), int(element[1])])

                if node not in hop_count:
                    hop_count[node] = []

                hop_count[node].append(raw_data)

            raw_data = []

        for node, data  in hop_count.iteritems():
            hop_count_data = [element[3] for repetition in data for element in repetition]

            self.data_min[node] = np.amin(hop_count_data)
            self.data_max[node] = np.amax(hop_count_data)
            self.data_median[node] = np.median(hop_count_data)
            self.data_std[node] = np.std(hop_count_data)
            self.data_avg[node] = np.average(hop_count_data)

            self.logger.info("Printing hop count statistics for node %s", node)
            self.logger.info("Minimum hop count = %f nodes", self.data_min[node])
            self.logger.info("Maximum hop count = %f nodes", self.data_max[node])
            self.logger.info("Std.Deviation     = %f nodes", self.data_std[node])
            self.logger.info("Average hop count = %f nodes", self.data_avg[node])
            self.logger.info("Median hop count  = %f nodes", self.data_median[node])
        if self.draw:            
            for node in hop_count:
                self.metric = "hop_count_node-" + str(node)
                self.plot_boxplot("Average Hop Count (Node " + str(node) + ")", "Repetition", "Hop Count [ms]", self.data_avg[node])

        if self.csv:
            self.export_csv()
            self.export_csv_raw(hop_count)

    def export_csv(self):
        self.metric = "hopCount"
        file_name = self.scenario + "_" + self.metric + "_aggregated.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - hop count for scenario ' + self.scenario],['# aggregated over ' + str(self.repetitions) + ' repetitions'],['#']]
        header = ['node', 'min', 'max', 'median', 'std', 'avg']

        data = []

        for node in self.data_min:
            data.append([node, self.data_min[node], self.data_max[node], self.data_median[node], self.data_std[node],  self.data_avg[node]])

        self._write_csv_file(file_name, disclaimer, header, data)

    def export_csv_raw(self, raw_data):
        self.metric = "hopCount"
        file_name = self.scenario + "_" + self.metric + ".csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - hop count for scenario ' + self.scenario],['#']]
        header = ['node', 'repetition', 'timestamp', 'hop count']

        data = []

        for node, hop_counts in raw_data.iteritems():
            for values in hop_counts:
                for element in values:
                    data.append([node, element[0], element[2], element[3]])
              
        self._write_csv_file(file_name, disclaimer, header, data)
