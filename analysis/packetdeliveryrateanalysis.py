#!/usr/bin/env python2.7

class PacketDeliveryRateAnalysis:

    def evaluate(self, experiment_results):
        self.nr_of_repetitions = experiment_results.get_number_of_repetitions()
        self.nr_of_sent_packets = experiment_results.get_average('trafficSent');
        self.nr_of_received_packets = experiment_results.get_average('trafficReceived')
        self.nr_of_detected_routing_loops = experiment_results.get_average('routingLoopDetected:count')
        self.nr_of_route_failures = experiment_results.get_average('routeFailure:count')
        self.nr_of_failed_route_discoveries = experiment_results.get_average('packetUnDeliverable:count')
        self.nr_of_expired_TTLs = experiment_results.get_average('dropZeroTTLPacket:count')
        self.nr_of_route_discoveries = experiment_results.get_average('newRouteDiscovery:count')
        self.inexplicable_loss = self.nr_of_sent_packets - self.nr_of_received_packets - self.nr_of_detected_routing_loops - self.nr_of_route_failures - self.nr_of_failed_route_discoveries - self.nr_of_expired_TTLs
        
        self._print_statistics()
        
    def _print_statistics(self):
        print "\nRunning PDR analysis.."
        print '=' * 55
        print "Overall statistics (averaged over %d iterations)" % self.nr_of_repetitions
        self.print_statistics("Sent Packets", self.nr_of_sent_packets, self.nr_of_sent_packets)
        self.print_statistics("Received Packets", self.nr_of_sent_packets, self.nr_of_received_packets)
        self.print_statistics("Routing Loops", self.nr_of_sent_packets, self.nr_of_detected_routing_loops)
        self.print_statistics("Route Failures", self.nr_of_sent_packets, self.nr_of_route_failures)
        self.print_statistics("Failed Route Discoveries", self.nr_of_sent_packets, self.nr_of_failed_route_discoveries)
        self.print_statistics("Dropped Packets (TTL = 0)", self.nr_of_sent_packets, self.nr_of_expired_TTLs)
        self.print_statistics("Inexplicable loss", self.nr_of_sent_packets, self.inexplicable_loss)
        print "\nAverage number of route discoveries: %d" % self.nr_of_route_discoveries

    def print_statistics(self, name, avg_nr_of_sent_packets, value):
        if avg_nr_of_sent_packets > 0:
            percent = "%6.2f%%" % ((value/float(avg_nr_of_sent_packets)) * 100.0)
        else:
            percent = "  0.00%%"
        
        max_number_of_digits = len(str(avg_nr_of_sent_packets))
        print "%-26s %*d\t" % (name, max_number_of_digits, value) + percent
