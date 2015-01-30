#!/usr/bin/env python2.7

import sys
import logging

import numpy as np

from .analysis import Analysis

class PacketDeliveryRateAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "pdr", repetitions, csv)
        self.logger = logging.getLogger('baltimore.analysis.PacketDeliveryRateAnalysis')
        self.logger.debug('creating an instance of PacketDeliveryRateAnalysis for scenario %s', scenario)
        self.all_pdr = []
        self.scenario = scenario

    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running PDR analysis..")

        if is_verbose:
            self.analyse_single_repetitions(experiment_results)
        self.check_no_inexplicable_loss(experiment_results)
        self.analyse_average_values(experiment_results)

        self._compute_pdr(experiment_results)
        self.get_packet_delivery_rate(experiment_results)

        if self.csv:
            self.export_csv()

        if self.draw:
            self.plot_boxplot("Packet Delivery Rate per Scenario", "", "Packet Delivery Rate", self.all_pdr)

    def _compute_pdr(self, results):
        for repetition in results:
            # don't count in the packets for which n route could be found
            nr_of_sent_packets = results.get_metric('trafficSent', repetition) - results.get_metric('packetUnDeliverable:count', repetition)
            if nr_of_sent_packets == 0:
                raise Exception("WARNING: All packets in repetition "+str(repetition)+" have been reported as undeliverable (very unlucky start scenario?)")

            pdr = results.get_metric('trafficReceived', repetition)/nr_of_sent_packets
            pdr = round(pdr*100, 2)
            self.all_pdr.append(pdr)


    def get_packet_delivery_rate(self, results):
        if len(self.all_pdr) == 0:
            self._compute_pdr(results)

        self.data_min = round(np.amin(self.all_pdr), 2)
        self.data_max = round(np.amax(self.all_pdr), 2)
        self.data_median = round(np.median(self.all_pdr), 2)
        self.data_std = round(np.std(self.all_pdr), 2)
        self.data_avg = round(np.average(self.all_pdr), 2)

        # TODO: cleanup
        self.pdr = self.data_avg

    def check_no_inexplicable_loss(self, result):
        for repetition in result:
            try:
                inexplicable_loss  = result.get_metric('trafficSent', repetition) - result.get_metric('trafficReceived', repetition)
                inexplicable_loss -= result.get_metric('routingLoopDetected:count', repetition)
                inexplicable_loss -= result.get_metric('packetUnDeliverable:count', repetition)
                inexplicable_loss -= result.get_metric('dropZeroTTLPacket:count', repetition)
                inexplicable_loss -= result.get_metric('routeFailure:count', repetition)
                inexplicable_loss -= result.get_metric('routeFailureNoHopAvailable:count', repetition)
                inexplicable_loss -= result.get_metric('routeFailureNextHopIsSender:count', repetition)
                inexplicable_loss -= result.get_metric('dropPacketBecauseEnergyDepleted:count', repetition)
            except KeyError:
                self.logger.error("there is no such metric in repetition %d", repetition)

            if inexplicable_loss > 0:
                sys.stderr.write("WARNING: The loss of %d packets could not be explained (Scenario %s)\n" % (inexplicable_loss, str(repetition)))

    def analyse_average_values(self, results):
        self.print_analysis_header(results)
        total_nr_of_packets = results.get_average('trafficSent')
        nr_of_undeliverables = results.get_average('packetUnDeliverable:count')
        nr_of_sent_packets = total_nr_of_packets - nr_of_undeliverables

        self._print_avg_statistics_line("Sent Packets",                      'trafficSent', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Received Packets",                  'trafficReceived', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Routing Loops",                     'routingLoopDetected:count', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Route Failures (all routes broke)", 'routeFailure:count', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Route Failures (no routes at all)", 'routeFailureNoHopAvailable:count', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Route Failures (next hop=sender)",  'routeFailureNextHopIsSender:count', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Dropped Packets (TTL = 0)", 'dropZeroTTLPacket:count', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Dropped Packets because 0 energy",  'dropPacketBecauseEnergyDepleted:count', results, nr_of_sent_packets)
        self._print_avg_statistics_line("Trapped packets after finish", 'nrOfTrappedPacketsAfterFinish', results, nr_of_sent_packets)

        print("Average number of route discoveries: %d" % results.get_average('newRouteDiscovery:count'))
        print("Average number of packets droped due to failed route discovery: %d (%s%%)\n" % (nr_of_undeliverables, self._get_percent_string(nr_of_undeliverables, total_nr_of_packets)))


    def _print_avg_statistics_line(self, name, metric_name, results, nr_of_sent_packets):
        nr_of_digits = self.get_max_nr_of_digits(nr_of_sent_packets)

        try:
            data_avg = results.get_average(metric_name)
            percent = self._get_percent_string(data_avg, nr_of_sent_packets)
            data_median = self._get_percent_string(results.get_median(metric_name), nr_of_sent_packets)
            data_std = self._get_percent_string(results.get_standard_deviation(metric_name), nr_of_sent_packets)
            data_min = self._get_percent_string(results.get_minimum(metric_name), nr_of_sent_packets)
            data_max = self._get_percent_string(results.get_maximum(metric_name), nr_of_sent_packets)

            print("%-34s %*d   %s   %s   %s   %s   %s" % (name, nr_of_digits, data_avg, percent, data_median, data_std, data_min, data_max))
        except KeyError:
            self.logger.error("there is no such metric " + metric_name)

    def analyse_single_repetitions(self, results):
        for repetition in results:
            print("Statistics of " + repetition.get_parameter('run'))
            self._print_statistics(results, repetition)

    def _print_statistics(self, results, repetition):
        print('=' * 55)
        self._print_statistics_line("Sent Packets",                      'trafficSent', results, repetition)
        self._print_statistics_line("Received Packets",                  'trafficReceived', results, repetition)
        self._print_statistics_line("Routing Loops",                     'routingLoopDetected:count', results, repetition)
        self._print_statistics_line("Route Failures (all routes broke)", 'routeFailure:count', results, repetition)
        self._print_statistics_line("Route Failures (no routes at all)", 'routeFailureNoHopAvailable:count', results, repetition)
        self._print_statistics_line("Route Failures (next hop=sender)",  'routeFailureNextHopIsSender:count', results, repetition)
        self._print_statistics_line("Failed Route Discoveries",          'packetUnDeliverable:count', results, repetition)
        self._print_statistics_line("Dropped Packets (TTL = 0)",         'dropZeroTTLPacket:count', results, repetition)
        self._print_statistics_line("Trapped packets after finish",      'nrOfTrappedPacketsAfterFinish', results, repetition)
        print("Number of route discoveries: %d\n" % results.get_metric('newRouteDiscovery:count', repetition))

    def _print_statistics_line(self, name, metric_name, results, repetition):
        nr_of_sent_packets = results.get_metric('trafficSent', repetition)
        nr_of_digits = self.get_max_nr_of_digits(nr_of_sent_packets)

        value = results.get_metric(metric_name, repetition)
        percent = self._get_percent_string(value, nr_of_sent_packets)

        print("%-26s %*d   %s" % (name, nr_of_digits, value, percent))

    def get_max_nr_of_digits(self, nr_of_packets):
        return len(str(nr_of_packets))


    def export_csv(self):
        file_name = self.scenario + "_" + self.metric + "_aggregated.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - packet delivery rate for scenario ' + self.scenario],['# aggregated over ' + str(self.repetitions) + ' repetitions'],['#']]
        header = ['min', 'max', 'median', 'std', 'avg']
        data = [[self.data_min, self.data_max, self.data_median, self.data_std,  self.data_avg]]

        self._write_csv_file(file_name, disclaimer, header, data)
        self._export_csv_raw()

    def _export_csv_raw(self):
        file_name = self.scenario + "_" + self.metric + ".csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - packet delivery rate for scenario ' + self.scenario + ' per repetition'],['#'],['#']]
        header = ['repetition', 'value']
        data = []

        for repetition, pdr in enumerate(self.all_pdr):
            data.append([repetition, pdr])

        self._write_csv_file(file_name, disclaimer, header, data)
