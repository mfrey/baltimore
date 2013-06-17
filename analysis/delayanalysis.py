#!/usr/bin/env python2.7

import sys
import numpy as np

class DelayAnalysis:
    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning delay analysis.."
	
	# determine the nodes 
	print experiment_results.get_average('delay')
#        for node_identifier, results in experiment_results.repetitions[0].get_node_results().iteritems():
#            print results[node_identifier]['delay'];

        
    #    if is_verbose:
    #        self.analyse_single_repetitions(experiment_results)
        
    #    self.check_no_inexplicable_loss(experiment_results)
    #    self.analyse_average_values(experiment_results)
    
