#!/usr/bin/env python2.7

import sys
import logging

import numpy as np
from scipy import stats

from analysis import Analysis

class OverheadAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "overhead", repetitions, csv)
        self.logger = logging.getLogger('baltimore.analysis.OverheadAnalysis')
        self.logger.debug('creating an instance of OverheadAnalysis for scenario %s', scenario)
        self.packet_overhead = []
        self.bit_overhead = []
        self.packet_statistics = {}
        self.bit_statistics = {}

    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running overhead analysis..")
        self.analyse_average_values(experiment_results)
        self._get_overhead(experiment_results)

        if self.csv:
            self.export_csv()

    # add support for bitwise overhead (and not only packetwise)
    def _compute_overhead(self, results):
        for repetition in results:
           data_packets = results.get_metric('nrOfDataPackets', repetition)
           control_packets = results.get_metric('nrOfControlPackets', repetition)
           all_packets = data_packets + control_packets
           self.packet_overhead.append(control_packets/all_packets)

           nr_of_data_bits = results.get_metric('nrOfSentDataBits', repetition)
           nr_of_control_bits = results.get_metric('nrOfSentControlBits', repetition)
           nr_of_all_bits = nr_of_data_bits + nr_of_control_bits
           self.bit_overhead.append(nr_of_control_bits/nr_of_all_bits)

    def _get_overhead(self, results):
        if len(self.packet_overhead) == 0:
            self._compute_overhead(results)

        self.packet_statistics['Min'] = round(np.amin(self.packet_overhead)*100, 2)
        self.packet_statistics['Max'] = round(np.amax(self.packet_overhead)*100, 2)
        self.packet_statistics['Med'] = round(np.median(self.packet_overhead)*100, 2)
        self.packet_statistics['Std'] = round(np.std(self.packet_overhead)*100, 2)
        self.packet_statistics['Avg'] = round(np.average(self.packet_overhead)*100, 2)
	self.packet_statistics['low'] = round(stats.scoreatpercentile(self.packet_overhead, 5)*100, 2)
        self.packet_statistics['hig'] = round(stats.scoreatpercentile(self.packet_overhead, 95)*100, 2)
        
        self.bit_statistics['Min'] = round(np.amin(self.bit_overhead)*100, 6)
        self.bit_statistics['Max'] = round(np.amax(self.bit_overhead)*100, 6)
        self.bit_statistics['Med'] = round(np.median(self.bit_overhead)*100, 6)
        self.bit_statistics['Avg'] = round(np.average(self.bit_overhead)*100, 6)
        self.bit_statistics['Std'] = round(np.std(self.bit_overhead)*100, 6)
        self.bit_statistics['low'] = round(stats.scoreatpercentile(self.bit_overhead, 5)*100, 6)
        self.bit_statistics['hig'] = round(stats.scoreatpercentile(self.bit_overhead, 95)*100, 6)

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

    def export_csv(self):
        file_name = self.scenario + "_" + self.metric + "_packets.csv"
	disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - overhead (packets) for scenario ' + self.scenario],['# aggregated over ' + str(self.repetitions) + ' repetitions'],['#']]
	header = ['min', 'max', 'median', 'std', 'avg', 'low', 'high']
	data = [[self.packet_statistics['Min'], self.packet_statistics['Max'], self.packet_statistics['Med'], self.packet_statistics['Std'], self.packet_statistics['Avg'], self.packet_statistics['low'], self.packet_statistics['hig']]]
        self._write_csv_file(file_name, disclaimer, header, data)

        # Write bit overhead to csv
        file_name = self.scenario + "_" + self.metric + "_bits.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - overhead (bits) for scenario ' + self.scenario],['# aggregated over ' + str(self.repetitions) + ' repetitions'],['#']]
        header = ['minimum', 'maximum', 'median', 'deviation', 'average', 'low', 'high']
        data = [[self.bit_statistics['Min'], self.bit_statistics['Max'], self.bit_statistics['Med'], self.bit_statistics['Std'], self.bit_statistics['Avg'], self.bit_statistics['low'], self.bit_statistics['hig']]]
        self._write_csv_file(file_name, disclaimer, header, data)

