#!/usr/bin/env python2.7

import os
import sys
import json
import runner
import logging
import itertools
import collections

from Queue import Empty
from multiprocessing import Process, Queue, Pool

from runner import Runner
from plot.packetdeliveryrateplot import PacketDeliveryRatePlot
from plot.boxplot import BoxPlot
from experiment import Experiment
from experimentmanagerworker import ExperimentManagerWorker
from persistence.baltimorejsonencoder import BaltimoreJSONEncoder
from persistence.baltimorejsondecoder import BaltimoreJSONDecoder
from parser.omnetconfigurationfileparser import OMNeTConfigurationFileParser

class ExperimentManager:
    def __init__(self, baltimore_revision, libara_revision):
        self.experiments = {}
        self.baltimore_revision = baltimore_revision
        self.libara_revision = libara_revision

    def check_result_files(self, directory, scenarios):
        result = self._check_result_directory_for_results(directory, scenarios)
        # probably a better way to do it
        non_existing_scenarios = [scenario[0] for scenario in result if scenario[1] == False]
        for scenario in non_existing_scenarios:
            print "There is no scenario", scenario, "to analyze!"
        # return a list of the remaining scenarios
        return list(set(scenarios) - set(non_existing_scenarios))

    def run_simulations(self, configuration):
        self.pool = Pool(configuration['cpu_cores'])
        # build up a tuple consisting of scenarios and repetitions
        argument = itertools.product(configuration['scenarios'], range(configuration['repetitions']), [configuration])
        # run the simulations
        self.pool.map(runner.run_simulation, argument)

    def process(self, configuration, is_verbose=False):
        directory = configuration['cwd']
        scenarios = configuration['scenarios']

        queue = Queue()
        jobs = []

        # single scenario to handle
        if len(scenarios) == 1 and scenarios[0] != '':
            process = ExperimentManagerWorker(configuration, scenarios[0], queue, is_verbose)
            jobs.append(process)
            process.start()
        # multiple scenarios in a directory
        else:
            if len(scenarios) == 1 and scenarios[0] == '':
                scenarios = self._get_scenarios(directory + '/results')

            for scenario in scenarios:
                process = ExperimentManagerWorker(configuration, scenario, queue, is_verbose)
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

        self.generate_packet_delivery_plots(configuration['analysis_location'])

#    def generate_delay_boxplots(self):
        #plot = BoxPlot()
        #plot.ylabel = "ms"

    def generate_packet_delivery_plots(self, location):
        scenario_list = [e for e in xrange(len(self.experiments))]
        pdr_list = []
        experiment_list = []
        experiments = collections.OrderedDict(sorted(self.experiments.items()))
        #for experiment in self.experiments:
        for experiment in experiments:
            experiment_list.append(experiment)
            pdr_list.append(self.experiments[experiment][1].pdr)
        plot = PacketDeliveryRatePlot()
        plot.xlist = [scenario_list]
        plot.xticklabels = experiment_list
        plot.ylist = [pdr_list]
        plot.draw(os.path.join(location, 'test.png'))

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

    def create_json(self):
        encoder = BaltimoreJSONEncoder()
        return encoder.encode(self)

    def write_json(self, file_name):
        data = self.crete_json()

        with open(file_name, 'w') as json_file:
            json.dump(data, json_file)

    def read_json(self, file_name):
        data = {}
        decoder = BaltimoreJSONDecoder()
        obj = []

        with open(file_name, 'r') as json_file:
            obj.append(json.load(json_file))

        ist = decoder.dict_to_object(obj)
        print ist
