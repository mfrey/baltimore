#!/usr/bin/env python2.7

class ExperimentResult:
    def __init__(self):
        self.repetitions = []
    
    def add_repetition(self, node_results):
        self.repetitions.append(node_results)
         
    #def get_average(self, metric_name):
        