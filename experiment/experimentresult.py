#!/usr/bin/env python2.7

class ExperimentResult:
    def __init__(self):
        self.repetitions = []
    
    def add_repetition(self, node_results):
        self.repetitions.append(node_results)
    
    def get_number_of_repetitions(self):
        return len(self.repetitions)
    
    def get_average(self, metric_name):
        #TODO: enable caching of calculated results
        overall_sum = 0
        for repetition_number, nodes in enumerate(self.repetitions):
            for node_identifier, results in nodes.iteritems():
                overall_sum += results[metric_name];

        nr_of_repetitions = self.get_number_of_repetitions()
        return overall_sum / float(nr_of_repetitions)