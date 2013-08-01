#!/usr/bin/env python2.7

import sys
import logging

import numpy as np

from analysis import Analysis

class OverheadAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions):
        Analysis.__init__(self, scenario, location, "overhead", repetitions)
        self.logger = logging.getLogger('baltimore.analysis.OverheadAnalysis')
        self.logger.debug('creating an instance of OverheadAnalysis for scenario %s', scenario)

    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running overhead analysis..")
        # TODO printout single repetition data
        self.analyse_average_values(experiment_results)

    # add support for bitwise overhead (and not only packetwise)
    def _compute_overhead(self, results):
        self.overhead = []

        for repetition in results:
           data_packets = results.get_metric('nrOfDataPackets', repetition)
           control_packets = results.get_metric('nrOfControlPackets', repetition)
           all_packets = data_packets + control_packets
           overhead.append(control_packets/all_packets)

    def _get_overhead(self, results):
        if len(self.overhead) == 0:
            self._compute_overhead(results)

        self.data_min = np.amin(self.overhead)
        self.data_max = np.amax(self.overhead)
        self.data_median = np.median(self.overhead)
        self.data_std = np.std(self.overhead)
        self.data_avg = np.average(self.overhead)
           

    def analyse_average_values(self, results):
        self.print_analysis_header(results)

        nr_of_data_packets = results.get_average('nrOfDataPackets')
        nr_of_control_packets = results.get_average('nrOfControlPackets')
        nr_of_all_packets = nr_of_data_packets + nr_of_control_packets
        print "%-34s %8d   100.00%%" % ("Number of all packets", nr_of_all_packets)

        self._print_avg_statistics_line("Number of data packets",  'nrOfDataPackets', results, nr_of_all_packets)
        self._print_avg_statistics_line("Number of control packets",  'nrOfControlPackets', results, nr_of_all_packets)

        nr_of_data_bits = results.get_average('nrOfSentDataBits')
        nr_of_control_bits = results.get_average('nrOfSentControlBits')
        nr_of_all_bits = nr_of_data_bits + nr_of_control_bits

        print
        print "%-34s %8d   100.00%%" % ("Number of total bits sent", nr_of_all_bits)

        self._print_avg_statistics_line("Number of data bits",  'nrOfSentDataBits', results, nr_of_all_bits)
        self._print_avg_statistics_line("Number of control bits",  'nrOfSentControlBits', results, nr_of_all_bits)


    def get_nr_of_all_packets(self, results):
        nr_of_data_packets = results.get_average('nrOfDataPackets')
        nr_of_control_packets = results.get_average('nrOfControlPackets')
        return nr_of_data_packets + nr_of_control_packets

    def _print_avg_statistics_line(self, name, metric_name, results, total):
        nr_of_digits = 8

        average_metric = results.get_average(metric_name)
        percent = self._get_percent_string(average_metric, total)
        median = self._get_percent_string(results.get_median(metric_name), total)
        std_deviation = self._get_percent_string(results.get_standard_deviation(metric_name), total)
        min = self._get_percent_string(results.get_minimum(metric_name), total)
        max = self._get_percent_string(results.get_maximum(metric_name), total)

        print "%-34s %*d   %s   %s   %s   %s   %s" % (name, nr_of_digits, average_metric, percent, median, std_deviation, min, max)
