#!/usr/bin/env python2.7

import os
import sys
import logging
import multiprocessing

from experiment import Experiment
from analysis.packetdeliveryrateanalysis import PacketDeliveryRateAnalysis 

class ExperimentManagerWorker(multiprocessing.Process):
    
    def __init__(self, directory, scenario_name, queue, is_verbose=False, visualize=False):
        super(ExperimentManagerWorker,self).__init__()
        self.directory = directory
        self.scenario_name = scenario_name
        self.verbose = is_verbose
        self.visualize = visualize
        self.results_queue = queue
    
    def run(self): 
        try:
            # TODO: change this to logging, so we only print it if required
            print 'Scanning directory "%s" for simulation result files.\nThis may take some time depending on the number of files...' % self.directory
            # TODO: use some kind of configuration to run more than one experiment
            experiment = Experiment(self.directory + '/results', self.scenario_name, self.visualize)
            experiment_results = experiment.get_results()
        
            # TODO: use some kind of configuration to run more than one analysis
            pdrAnalyser = PacketDeliveryRateAnalysis()
            pdrAnalyser.evaluate(experiment_results, self.verbose)
            
            # TODO: change this to logging, so we only print it if required
            nr_of_parsed_files = experiment_results.get_number_of_repetitions()
            print "\n\nSuccessfully read %d experiment(s) from %d scalar file(s)." % (1, nr_of_parsed_files)
            
            # store the result
            self.results_queue.put((experiment, pdrAnalyser))
        except Exception as exception:
            print "An error occurred while evaluating experiment", self.scenario_name, ": ", exception
