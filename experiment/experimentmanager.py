#!/usr/bin/env python2.7

import os
import json
import runner
import logging
import itertools

from Queue import Empty

from multiprocessing import Queue, Pool

from experimentmanagerworker import ExperimentManagerWorker
from persistence.baltimorejsonencoder import BaltimoreJSONEncoder
from persistence.baltimorejsondecoder import BaltimoreJSONDecoder
from parser.omnetconfigurationfileparser import OMNeTConfigurationFileParser

class ExperimentManager:
    def __init__(self, baltimore_revision, libara_revision):
        self.logger = logging.getLogger('baltimore.experiment.ExperimentManager')
        self.logger.debug('creating an instance of ExperimentManager')
        self.baltimore_revision = baltimore_revision
        self.libara_revision = libara_revision

    def check_result_files(self, directory, scenarios):
        result = self._check_result_directory_for_results(directory, scenarios)
        non_existing_scenarios = [scenario[0] for scenario in result if scenario[1] == False]

        for scenario in non_existing_scenarios:
            self.logger.error("There is no scenario " + scenario + " to analyze!")
        # return a list of the remaining scenarios
        return list(set(scenarios) - set(non_existing_scenarios))

    def run_simulations(self, configuration):
        ned_path_raw = configuration['ned_path']
        omnetpp_ini_raw = configuration['omnetpp_ini']

        self.pool = Pool(configuration['cpu_cores'])
        for experiment in configuration['experiments']:
            scenarios = experiment[0]
            self.logger.debug("scenarios " + str(scenarios))
            
            location = experiment[1]
            configuration['repetitions'] = experiment[2]
            configuration['ned_path'] = ned_path_raw + configuration['ara_home'] + '/simulations/' + location 
            configuration['omnetpp_ini'] = omnetpp_ini_raw + location + '/omnetpp.ini'
            
            # build up a tuple consisting of scenarios and repetitions
            argument = itertools.product(scenarios, range(experiment[2]), [configuration], [location])
            # run the simulations
            self.pool.map(runner.run_simulation, argument)

    def process(self, configuration, experiment, scenarios, arguments):
        is_verbose = arguments.verbose
        directory = configuration['cwd'] + '/' + experiment

        if os.path.exists(directory + '/omnetpp.ini'):
            self.read_omnetppini(directory + '/omnetpp.ini', is_verbose)
            
            if is_verbose:
                self._print_general_settings(self.omnetpp_ini.get_section('General'))

        queue = Queue()
        jobs = []

        # single scenario to handle
        if len(scenarios) == 1 and scenarios[0] != '':
            process = ExperimentManagerWorker(configuration, experiment, scenarios[0], queue, arguments)
            jobs.append(process)
            process.start()
        # multiple scenarios in a directory
        else:
            if len(scenarios) == 1 and scenarios[0] == '':
                scenarios = self._get_scenarios(directory + '/results')

            for scenario in scenarios:
                process = ExperimentManagerWorker(configuration, experiment, scenario, queue, arguments)
                jobs.append(process)
                process.start()

        # storing the results in an class attribute
        for job in jobs:
            job.join()

            try:
                result = queue.get(True)
                self.logger.debug("The process " + job.scenario_name + " returned with the status " + result)
            except Empty:
                self.logger.error("Could not retrieve result data for scenario " + job.scenario_name + " (might have failed earlier)")

    def read_omnetppini(self, file_path, is_verbose):
        # TODO throw error if verbose = True
        self.omnetpp_configuration = OMNeTConfigurationFileParser(file_path)
        self.omnetpp_ini = self.omnetpp_configuration.get_section("General")

        self.omnetpp_ini_checksum = self.omnetpp_configuration.omnetpp_ini_hash
        self.standard_ini_checksum = self.omnetpp_configuration.standard_ini_hash

    def _get_scenarios(self, directory):
        scenarios = []
        for file_name in os.listdir(directory):
            if file_name.endswith('sca'):
                scenario = file_name.split('-')[0]
                if scenario not in scenarios:
                    scenarios.append(scenario)
        return scenarios

    def _check_result_directory_for_results(self, directory, scenarios):
        existing_scenarios = self._get_scenarios(directory)
        return [(scenario, scenario in existing_scenarios) for scenario in scenarios]

    def check_result_directory(self, directory, scenarios):
        existing_scenarios = self._get_scenarios(directory)
        for scenario in scenarios:
            if scenario in existing_scenarios:
                print "There seems already to be a scenario ", scenario, " in the results directory"
                reply = raw_input("Shall the existing scenario be removed? [Y/n] ").lower()
                if reply.startswith("y"):
                    self._remove_scenario(directory, scenario)

    def _remove_scenario(self, directory, scenario):
        files = [f for f in os.listdir(directory) if f.startswith(scenario + "-")]
        for f in files:
            os.remove(directory + '/' + f)

    def result_dir_exists(self, directory):
        if not os.path.exists(directory + '/results'):
            os.makedirs(directory + '/results')
            return False
        return True

    def _print_general_settings(self, general_settings):
        self._print_tuple(general_settings)

    def _print_scenario_settings(self, scenario_settings):
        self._print_tuple(scenario_settings)

    def _print_tuple(self, settings):
        for setting in settings:
            print setting[0], ' = ', setting[1]

    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d        

    def __setstate__(self, d):
        self.__dict__.update(d)
