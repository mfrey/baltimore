#!/usr/bin/env python2.7

import sys

class OverheadAnalysis:

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning Overhead analysis.."
        
        # TODO printout single repetition data
        self.analyse_average_values(experiment_results)
    
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
    
    def print_analysis_header(self, results):
        nr_of_repetitions = results.get_number_of_repetitions()
        print "Overall statistics (averaged over %d iterations)" % nr_of_repetitions
        print '=' * 100
        print " " * 42 + "#   Average    Median   Std.Dev       Min       Max"
        print '-' * 100
    
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
        
    def _get_percent_string(self, value, nr_of_packets):
        if nr_of_packets > 0:
            return "%6.2f%%" % ((value/float(nr_of_packets)) * 100.0)
        else:
            return "  0.00%%"
