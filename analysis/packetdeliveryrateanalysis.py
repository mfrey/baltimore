#!/usr/bin/env python2.7

class PacketDeliveryRateAnalysis:

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning PDR analysis.."
        
        if is_verbose:
            self.analyse_single_repetitions(experiment_results)
        
        self.analyse_average_values(experiment_results)
    
    def analyse_average_values(self, experiment_results):
        nr_of_repetitions = experiment_results.get_number_of_repetitions()
        print "Overall statistics (averaged over %d iterations)" % nr_of_repetitions
        
        average_results = {'sent': experiment_results.get_average('trafficSent'),
                           'received': experiment_results.get_average('trafficReceived'),
                           'loops': experiment_results.get_average('routingLoopDetected:count'),
                           'route_failures': experiment_results.get_average('routeFailure:count'),
                           'failed_discoveries': experiment_results.get_average('packetUnDeliverable:count'),
                           'expired_TTLs': experiment_results.get_average('dropZeroTTLPacket:count'),
                           'route_discoveries': experiment_results.get_average('newRouteDiscovery:count')}
        average_results['inexplicable'] = self.calculate_inexplicable_loss(average_results)        
        self._print_all_statistics(average_results)
    
    def analyse_single_repetitions(self, experiment_results):
        for repetition in experiment_results:
            print "Statistics of " + repetition.get_parameter('run')
            
            results = {'sent': experiment_results.get_metric('trafficSent', repetition),
                       'received': experiment_results.get_metric('trafficReceived', repetition),
                       'loops': experiment_results.get_metric('routingLoopDetected:count', repetition),
                       'route_failures': experiment_results.get_metric('routeFailure:count', repetition),
                       'failed_discoveries': experiment_results.get_metric('packetUnDeliverable:count', repetition),
                       'expired_TTLs': experiment_results.get_metric('dropZeroTTLPacket:count', repetition),
                       'route_discoveries': experiment_results.get_metric('newRouteDiscovery:count', repetition)}
            results['inexplicable'] = self.calculate_inexplicable_loss(results)
            self._print_all_statistics(results)
            
    def calculate_inexplicable_loss(self, results):
        return results['sent'] - results['received'] - results['loops'] - results['route_failures'] - results['failed_discoveries'] - results['expired_TTLs']
    
    def _print_all_statistics(self, results):
        print '=' * 55
        self._print_statistics("Sent Packets",              results['sent'], results['sent'])
        self._print_statistics("Received Packets",          results['sent'], results['received'])
        self._print_statistics("Routing Loops",             results['sent'], results['loops'])
        self._print_statistics("Route Failures",            results['sent'], results['route_failures'])
        self._print_statistics("Failed Route Discoveries",  results['sent'], results['failed_discoveries'])
        self._print_statistics("Dropped Packets (TTL = 0)", results['sent'], results['expired_TTLs'])
        self._print_statistics("Inexplicable loss",         results['sent'], results['inexplicable'])
        print "Number of route discoveries:  %d\n" % results['route_discoveries']

    def _print_statistics(self, name, nr_of_sent_packets, value):
        if nr_of_sent_packets > 0:
            percent = "%6.2f%%" % ((value/float(nr_of_sent_packets)) * 100.0)
        else:
            percent = "  0.00%%"
        
        max_number_of_digits = len(str(nr_of_sent_packets))
        print "%-26s %*d\t" % (name, max_number_of_digits, value) + percent
