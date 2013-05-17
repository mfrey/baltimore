#!/usr/bin/env python2.7

import os
import sys
import logging

from experiment import Experiment
from analysis.packetdeliveryrateanalysis import PacketDeliveryRateAnalysis 

class ExperimentManager:
    def __init__(self):
        self.experiments = {}

    def _get_scenarios(self, directory):
	  scenarios = []
	  for file_name in os.listdir(directory):
		if file_name.endswith('sca'):
		  scenario = file_name.split('-')[0]
		  if scenario not in scenarios:
			scenarios.append(scenario)

	  return scenarios

    def process(self, directory, scenario, is_verbose=False, visualize=False):
	  if scenario != "":
		self._process_scenario(directory, scenario, is_verbose, visualize)
	  else:
		scenarios = self._get_scenarios(directory + '/results')

		for s in scenarios:
		  self._process_scenario(directory, s, is_verbose, visualize)

    def _process_scenario(self, directory, scenario, is_verbose=False, visualize=False): 
        # TODO: change this to logging, so we only print it if required
        print 'Scanning directory "%s" for simulation result files.\nThis may take some time depending on the number of files...' % directory
        
        # TODO: use some kind of configuration to run more than one experiment
        experiment = Experiment(directory + '/results', scenario, visualize)
        experiment_results = experiment.get_results()
        
        # TODO: use some kind of configuration to run more than one analysis
        pdrAnalyser = PacketDeliveryRateAnalysis()
        pdrAnalyser.evaluate(experiment_results, is_verbose)
        
        # TODO: change this to logging, so we only print it if required
        nr_of_parsed_files = experiment_results.get_number_of_repetitions()
        print "\n\nSuccessfully read %d experiment(s) from %d scalar file(s)." % (1, nr_of_parsed_files)

        # we are going most likely to store also the result data
        self.experiments[scenario] = experiment

   
