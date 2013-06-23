#!/usr/bin/env python2.7

import os
import sys
import logging
import multiprocessing

from experiment import Experiment
from analysis.packetdeliveryrateanalysis import PacketDeliveryRateAnalysis
from analysis.overheadanalysis import OverheadAnalysis
from analysis.delayanalysis import DelayAnalysis

class ExperimentManagerWorker(multiprocessing.Process):

    def __init__(self, configuration, scenario_name, queue, is_verbose=False):
        super(ExperimentManagerWorker,self).__init__()
        self.simulations_directory = configuration['cwd']
        self.scenario_name = scenario_name
        self.verbose = is_verbose
        self.visualize = configuration['analysis_network']
        self.results_queue = queue
        self.routing_table_trace = configuration['analysis_routing_table_trace']

        if configuration['analysis_location'] == "":
            self.location = self.simulations_directory
        else:
            self.location = configuration['analysis_location']

    def run(self):
        try:
            # TODO: change this to logging, so we only print it if required
            print 'Scanning directory "%s" for simulation result files.\nThis may take some time depending on the number of files...' % self.simulations_directory
            # TODO: use some kind of configuration to run more than one experiment
            experiment = Experiment(self.simulations_directory + '/results', self.scenario_name, self.visualize, self.routing_table_trace, self.location)
            experiment_results = experiment.get_results()

            # TODO: use some kind of configuration to run more specific analysations
            pdrAnalyser = PacketDeliveryRateAnalysis(self.scenario_name)
            pdrAnalyser.get_packet_delivery_rate(experiment_results)
            pdrAnalyser.evaluate(experiment_results, self.verbose)

            overheadAnalyser = OverheadAnalysis()
            overheadAnalyser.evaluate(experiment_results, self.verbose)

            delayAnalyser = DelayAnalysis(self.scenario_name, self.location)
            delayAnalyser.evaluate(experiment_results, self.verbose)

            # TODO: change this to logging, so we only print it if required
            nr_of_parsed_files = experiment_results.get_number_of_repetitions()
            print "\n\nSuccessfully read %d experiment(s) from %d scalar file(s)." % (1, nr_of_parsed_files)

            # store the result
            self.results_queue.put((experiment, pdrAnalyser))
        except Exception as exception:
            print "An error occurred while evaluating experiment", self.scenario_name, ": ", exception
