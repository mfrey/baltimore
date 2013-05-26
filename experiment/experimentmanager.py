#!/usr/bin/env python2.7

import os
import sys
import logging
import itertools
import runner

from Queue import Empty
from multiprocessing import Process, Queue, Pool

from runner import Runner
from plot.packetdeliveryrateplot import PacketDeliveryRatePlot
from experiment import Experiment
from experimentmanagerworker import ExperimentManagerWorker
from persistence.baltimorejsonencoder import BaltimoreJSONEncoder
from parser.omnetconfigurationfileparser import OMNeTConfigurationFileParser

class ExperimentManager:
    def __init__(self):
        self.experiments = {}

    def run_simulations(self, configuration):
        self.pool = Pool(configuration['cpu_cores'])
	    # build up a tuple consisting of scenarios and repetitions
        argument = itertools.product(configuration['scenarios'], range(configuration['repetitions']), [configuration])
        # run the simulations
        self.pool.map(runner.run_simulation, argument)

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

            for scenario in scenarios:
                process = ExperimentManagerWorker(directory, scenario, queue, is_verbose, visualize) 
                jobs.append(process)
                process.start()

        omnetpp_ini = OMNeTConfigurationFileParser(directory + '/omnetpp.ini')

        # FIXME: that's a bug if no config.ini file is added
        if is_verbose:
            self._print_general_settings(omnetpp_ini.get_section('General'))

        # storing the results in an class attribute
        for job in jobs:
            job.join()
            # TODO: It might be better to remove the try/except and put an error code in the code (by the producer)
            # instead over an timeout
            try:
                result = queue.get(True, 1)
                self.experiments[result[0].scenario_name] = result

                # FIXME: that's a bug if no config.ini file is added
                if is_verbose:
                    self._print_scenario_settings(omnetpp_ini.get_scenario(result[0].scenario_name))

            except Empty:
                print "Could not retrieve result data for scenario", job.scenario_name, "(might have failed earlier)"

        self.generate_packet_delivery_plots()
        
    def generate_packet_delivery_plots(self):
        scenario_list = [e for e in xrange(len(self.experiments))]
        pdr_list = []
        for experiment in self.experiments:
            pdr_list.append(self.experiments[experiment][1].pdr)
        plot = PacketDeliveryRatePlot()
        plot.xlist = [scenario_list]
        plot.ylist = [pdr_list]
        plot.draw('test.png')

    def _get_scenarios(self, directory):
        scenarios = []
        for file_name in os.listdir(directory):
            if file_name.endswith('sca'):
                scenario = file_name.split('-')[0]
                if scenario not in scenarios:
                    scenarios.append(scenario)
        return scenarios

    def _print_general_settings(self, general_settings):
        self._print_tuple(general_settings)

    def _print_scenario_settings(self, scenario_settings):
        self._print_tuple(scenario_settings)

    def _print_tuple(self, settings):
        for setting in settings:
            print setting[0], ' = ', setting[1]
        
    def write_json(self, filename):
        encoder = BaltimoreJSONEncoder()
        print encoder.encode(self.experiments)
