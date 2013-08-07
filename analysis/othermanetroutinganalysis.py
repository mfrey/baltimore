#!/usr/bin/env python2.7

import sys
import logging

import numpy as np

from analysis import Analysis

class OtherManetRoutingAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "pdr", repetitions, csv)
        self.logger = logging.getLogger('baltimore.analysis.OtherManetRoutingAnalysis')

    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running analysis for other MANET routing protocol..")
        self.analyse_average_values(experiment_results)

    def analyse_average_values(self, results):
        self.print_analysis_header(results)
        self._print_avg_statistics_line("Sent Packets",     'sentPk:count', results)
        self._print_avg_statistics_line("Received Packets", 'rcvdPk:count', results)

    def _print_avg_statistics_line(self, name, metric_name, results):
        nr_of_sent_packets = results.get_average('sentPk:count')
        nr_of_digits = self.get_max_nr_of_digits(nr_of_sent_packets)

        try:
            data_avg = results.get_average(metric_name)
            percent = self._get_percent_string(data_avg, nr_of_sent_packets)
            data_median = self._get_percent_string(results.get_median(metric_name), nr_of_sent_packets)
            data_std = self._get_percent_string(results.get_standard_deviation(metric_name), nr_of_sent_packets)
            data_min = self._get_percent_string(results.get_minimum(metric_name), nr_of_sent_packets)
            data_max = self._get_percent_string(results.get_maximum(metric_name), nr_of_sent_packets)

            print "%-34s %*d   %s   %s   %s   %s   %s" % (name, nr_of_digits, data_avg, percent, data_median, data_std, data_min, data_max)
        except KeyError:
            self.logger.error("there is no such metric " + metric_name)

    def get_max_nr_of_digits(self, nr_of_packets):
        return len(str(nr_of_packets))
