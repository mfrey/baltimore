#!/usr/bin/env python2.7

import numpy as np

class ExperimentResult:
    def __init__(self):
        self.repetitions = {}
    
    def add_repetition(self, node_results):
        repetition = int(node_results.get_parameter("runnumber"))

        if repetition in self.repetitions.keys():
            for node in node_results.get_node_results().keys():
                for metric, result in node_results.get_node_results()[node].iteritems():
                    if node not in self.repetitions[repetition].get_node_results().keys():
                        self.repetitions[repetition].get_node_results()[node] = {}
                    self.repetitions[repetition].get_node_results()[node][metric] = result
        else: 
            self.repetitions[repetition] = node_results

    
    def get_number_of_repetitions(self):
        return len(self.repetitions)
    
    def get_average(self, metric_name):
        return np.average([self.get_metric(metric_name, repetition) for repetition in self.repetitions])
    
    def __iter__(self):
        return iter(self.repetitions)
    
    def get_metric(self, metric_name, repetition):
        sum = 0
        for node_identifier, results in self.repetitions[repetition].get_node_results().iteritems():
            sum += results[metric_name];
        
        return sum
    
    def get_minimum(self, metric_name):
        return np.amin([self.get_metric(metric_name, repetition) for repetition in self.repetitions])

    def get_maximum(self, metric_name):
        return np.amax([self.get_metric(metric_name, repetition) for repetition in self.repetitions])
    
    def get_median(self, metric_name):
        return np.median([self.get_metric(metric_name, repetition) for repetition in self.repetitions])
    
    def get_standard_deviation(self, metric_name):
        return np.std([self.get_metric(metric_name, repetition) for repetition in self.repetitions])

    def get_variance(self, metric_name):
        return np.var([self.get_metric(metric_name, repetition) for repetition in self.repetitions])
       
