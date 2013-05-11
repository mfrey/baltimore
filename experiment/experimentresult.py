#!/usr/bin/env python2.7

class ExperimentResult:
    def __init__(self):
        self.repetitions = []
    
    def add_repetition(self, node_results):
        self.repetitions.append(node_results)
    
    def get_number_of_repetitions(self):
        return len(self.repetitions)
    
    def get_average(self, metric_name):
        nr_of_repetitions = self.get_number_of_repetitions()
        if self.repetitions == 0:
            return 0
        
        #TODO: enable caching of calculated results
        overall_sum = 0
        for repetition in self.repetitions:
            overall_sum += self.get_metric(metric_name, repetition);

        return overall_sum / float(nr_of_repetitions)
    
    def __iter__(self):
        return iter(self.repetitions)
    
    def get_metric(self, metric_name, repetition):
        sum = 0
        for node_identifier, results in repetition.get_node_results().iteritems():
            sum += results[metric_name];
        
        return sum