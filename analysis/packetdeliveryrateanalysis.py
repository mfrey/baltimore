#!/usr/bin/env python2.7

import sys

from plot.boxplot import BoxPlot

class PacketDeliveryRateAnalysis:
    def __init__(self, scenario):
        self.all_pdr = []
        self.scenario = scenario


    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning PDR analysis.."

        if is_verbose:
            self.analyse_single_repetitions(experiment_results)
        self.check_no_inexplicable_loss(experiment_results)
        self.analyse_average_values(experiment_results)

        for repetition in experiment_results:
            pdr = experiment_results.get_metric('trafficReceived', repetition)/experiment_results.get_metric('trafficSent', repetition)
            self.all_pdr.append(pdr)

        # make a pdr box plot over all repetitions
        plot = BoxPlot()
        plot.title = "Packet Delivery Rate per Scenario"
        plot.ylabel = "Packet Delivery Rate"
        plot.draw(self.all_pdr, self.scenario + "_pdr.png")


    def get_packet_delivery_rate(self, results):
        avg_traffic_sent = results.get_average("trafficSent")
        avg_traffic_received = results.get_average("trafficReceived")
        self.pdr = float(avg_traffic_received/avg_traffic_sent)

    def check_no_inexplicable_loss(self, result):
        for repetition in result:
            inexplicable_loss  = result.get_metric('trafficSent', repetition) - result.get_metric('trafficReceived', repetition)
            inexplicable_loss -= result.get_metric('routingLoopDetected:count', repetition)
            inexplicable_loss -= result.get_metric('packetUnDeliverable:count', repetition)
            inexplicable_loss -= result.get_metric('dropZeroTTLPacket:count', repetition)
            inexplicable_loss -= result.get_metric('routeFailure:count', repetition)
            inexplicable_loss -= result.get_metric('routeFailureNoHopAvailable:count', repetition)
            inexplicable_loss -= result.get_metric('routeFailureNextHopIsSender:count', repetition)

            try:
                inexplicable_loss -= result.get_metric('dropPacketBecauseEnergyDepleted:count', repetition)
            except KeyError:
                print "there is no such metric dropPacketBecauseEnergyDepleted:count"

            if inexplicable_loss > 0:
                sys.stderr.write('~' * 74 + "\n")
                sys.stderr.write("WARNING: The loss of %d packets could not be explained (bug in simulation?)\n" % inexplicable_loss)
                sys.stderr.write("Scenario: " + str(repetition) + "\n");
                sys.stderr.write('~' * 74 + "\n\n")

    def analyse_average_values(self, results):
        nr_of_repetitions = results.get_number_of_repetitions()
        print "Overall statistics (averaged over %d iterations)" % nr_of_repetitions
        print '=' * 100
        print " " * 41 + "#   Average    Median   Std.Dev       Min       Max"
        print '-' * 100
        self._print_avg_statistics_line("Sent Packets",                      'trafficSent', results)
        self._print_avg_statistics_line("Received Packets",                  'trafficReceived', results)
        self._print_avg_statistics_line("Routing Loops",                     'routingLoopDetected:count', results)
        self._print_avg_statistics_line("Route Failures (all routes broke)", 'routeFailure:count', results)
        self._print_avg_statistics_line("Route Failures (no routes at all)", 'routeFailureNoHopAvailable:count', results)
        self._print_avg_statistics_line("Route Failures (next hop=sender)",  'routeFailureNextHopIsSender:count', results)
        self._print_avg_statistics_line("Failed Route Discoveries",  'packetUnDeliverable:count', results)
        self._print_avg_statistics_line("Dropped Packets (TTL = 0)", 'dropZeroTTLPacket:count', results)
        self._print_avg_statistics_line("Dropped Packets because 0 energy",  'dropPacketBecauseEnergyDepleted:count', results)
        self._print_avg_statistics_line("Trapped packets after finish", 'nrOfTrappedPacketsAfterFinish', results)
        print "Average number of route discoveries: %d\n" % results.get_average('newRouteDiscovery:count')

    def _print_avg_statistics_line(self, name, metric_name, results):
        nr_of_sent_packets = results.get_average('trafficSent')
        nr_of_digits = self.get_max_nr_of_digits(nr_of_sent_packets)

        try:
            average_metric = results.get_average(metric_name)
            percent = self._get_percent_string(average_metric, nr_of_sent_packets)
            median = self._get_percent_string(results.get_median(metric_name), nr_of_sent_packets)
            std_deviation = self._get_percent_string(results.get_standard_deviation(metric_name), nr_of_sent_packets)
            min = self._get_percent_string(results.get_minimum(metric_name), nr_of_sent_packets)
            max = self._get_percent_string(results.get_maximum(metric_name), nr_of_sent_packets)

            print "%-34s %*d   %s   %s   %s   %s   %s" % (name, nr_of_digits, average_metric, percent, median, std_deviation, min, max)
        except KeyError:
            print "there is no such metric ", metric_name

    def _print_calculated_statistics_line(self, name, value, results):
        nr_of_sent_packets = results.get_average('trafficSent')
        nr_of_digits = self.get_max_nr_of_digits(nr_of_sent_packets)
        print "%-26s %*d   %s" % (name, nr_of_digits, value, percent)

    def _get_percent_string(self, value, nr_of_packets):
        if nr_of_packets > 0:
            return "%6.2f%%" % ((value/float(nr_of_packets)) * 100.0)
        else:
            return "  0.00%%"

    def analyse_single_repetitions(self, results):
        for repetition in results:
            print "Statistics of " + repetition.get_parameter('run')
            self._print_statistics(results, repetition)

    def _print_statistics(self, results, repetition):
        print '=' * 55
        self._print_statistics_line("Sent Packets",                      'trafficSent', results, repetition)
        self._print_statistics_line("Received Packets",                  'trafficReceived', results, repetition)
        self._print_statistics_line("Routing Loops",                     'routingLoopDetected:count', results, repetition)
        self._print_statistics_line("Route Failures (all routes broke)", 'routeFailure:count', results, repetition)
        self._print_statistics_line("Route Failures (no routes at all)", 'routeFailureNoHopAvailable:count', results, repetition)
        self._print_statistics_line("Route Failures (next hop=sender)",  'routeFailureNextHopIsSender:count', results, repetition)
        self._print_statistics_line("Failed Route Discoveries",          'packetUnDeliverable:count', results, repetition)
        self._print_statistics_line("Dropped Packets (TTL = 0)",         'dropZeroTTLPacket:count', results, repetition)
        self._print_statistics_line("Trapped packets after finish",      'nrOfTrappedPacketsAfterFinish', results, repetition)
        print "Number of route discoveries: %d\n" % results.get_metric('newRouteDiscovery:count', repetition)

    def _print_statistics_line(self, name, metric_name, results, repetition):
        nr_of_sent_packets = results.get_metric('trafficSent', repetition)
        nr_of_digits = self.get_max_nr_of_digits(nr_of_sent_packets)

        value = results.get_metric(metric_name, repetition)
        percent = self._get_percent_string(value, nr_of_sent_packets)

        print "%-26s %*d   %s" % (name, nr_of_digits, value, percent)

    def get_max_nr_of_digits(self, nr_of_packets):
        return len(str(nr_of_packets))

