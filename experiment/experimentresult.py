#!/usr/bin/env python2.7
from numpy.ma.core import sqrt

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
    
    def get_minimum(self, metric_name):
        minimum = None
        for repetition in self.repetitions:
            candidate = self.get_metric(metric_name, repetition)
            if(minimum is None or candidate < minimum):
                minimum = candidate
            
        return minimum

    def get_maximum(self, metric_name):
        maximum = None
        for repetition in self.repetitions:
            candidate = self.get_metric(metric_name, repetition)
            if(maximum is None or candidate > maximum):
                maximum = candidate
            
        return maximum
    
    def get_median(self, metric_name):
        all_values = sorted(self.get_metric(metric_name, repetition) for repetition in self.repetitions)
        nr_of_values = len(all_values)
        if nr_of_values == 1:
            return all_values[0]
        elif nr_of_values % 2 == 0:
            # There is no single median so we calculate the average of the two median candidates
            # note that the arrays are zero based
            first_median = all_values[(nr_of_values/2) -1]
            second_median = all_values[((nr_of_values+2)/2) -1]
            return (first_median + second_median) / 2
        else:
            # just take the one element in the middle of the sorted list
            return all_values[(nr_of_values+1)/2]
    
    def get_standard_deviation(self, metric_name):
        average = self.get_average(metric_name)
        sum_of_square_differences = 0
        for repetition in self.repetitions:
            value = self.get_metric(metric_name, repetition)
            difference = (value - average)**2
            sum_of_square_differences += difference
        
        nr_of_repetitions = self.get_number_of_repetitions()
        std_deviation = sqrt(sum_of_square_differences/float(nr_of_repetitions))
        return std_deviation
    