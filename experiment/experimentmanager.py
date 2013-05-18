#!/usr/bin/env python2.7

import os
import sys
import logging
import multiprocessing

from experiment import Experiment
from experimentmanagerworker import ExperimentManagerWorker
from persistence.baltimorejsonencoder import BaltimoreJSONEncoder

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
		jobs = []
		scenarios = self._get_scenarios(directory + '/results')

		for s in scenarios:
		  process = ExperimentManagerWorker(directory, s, is_verbose, visualize) 
		  jobs.append(process)
		  process.start()

    def write_json(self, filename):
	  encoder = BaltimoreJSONEncoder()
	  print encoder.encode(self.experiments)
