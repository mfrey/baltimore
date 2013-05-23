#!/usr/bin/env python2.7

import os
import sys
import logging
import itertools

from Queue import Empty
from multiprocessing import Process, Queue, Pool

from runner import Runner, run_simulation
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

    def run_simulations(self, configuration):
        self.pool = Pool()
	# build up a tuple consisting of scenarios and repetitions
        argument = itertools.product(configuration['scenarios'], range(configuration['repetitions']), [configuration])
        # run the simulations
        self.pool.map(run_simulation, argument)

    def process(self, directory, scenarios, is_verbose=False, visualize=False):
        queue = Queue()
        jobs = []

        # single scenario to handle
        if len(scenarios) == 1 and scenarios[0] != '': 
            process = ExperimentManagerWorker(directory, scenarios[0], queue, is_verbose, visualize)
            jobs.append(process)
            process.start()
        # multiple scenarios in a directory
        else:
            if len(scenarios) == 1 and scenarios[0] == '':
                scenarios = self._get_scenarios(directory + '/results')

            print scenarios

            for scenario in scenarios:
                process = ExperimentManagerWorker(directory, scenario, queue, is_verbose, visualize) 
                jobs.append(process)
                process.start()

        # storing the results in an class attribute
        for job in jobs:
            job.join()
            # TODO: It might be better to remove the try/except and put an error code in the code (by the producer)
            # instead over an timeout
            try:
                result = queue.get(True, 1)
                self.experiments[result[0].scenario_name] = result
            except Empty:
                print "no entry in queue for scenario ", job.scenario
                print self.experiments


    def write_json(self, filename):
	  encoder = BaltimoreJSONEncoder()
	  print encoder.encode(self.experiments)
