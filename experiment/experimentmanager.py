#!/usr/bin/env python2.7

import os
import sys
import logging

from experiment import Experiment
from analysis.packetdeliveryrateanalysis import PacketDeliveryRateAnalysis 

class ExperimentManager:
    def __init__(self):
        self.experiments = {}
    
    def process(self, directory, scenario): 
        # TODO: change this to logging, so we only print it if required
        print 'Scanning directory "%s" for simulation result files.\nThis may take some time depending on the number of files...' % directory
        
        # TODO: use some kind of configuration to run more than one experiment
        experiment = Experiment(directory + '/results', scenario)
        experiment_results = experiment.get_results()
        
        # TODO: use some kind of configuration to run more than one analysis
        pdrAnalyser = PacketDeliveryRateAnalysis()
        pdrAnalyser.evaluate(experiment_results)
        
        # TODO: change this to logging, so we only print it if required
        nr_of_parsed_files = experiment_results.get_number_of_repetitions()
        print "\n\nSuccessfully read %d experiment(s) from %d scalar file(s)." % (1, nr_of_parsed_files)
