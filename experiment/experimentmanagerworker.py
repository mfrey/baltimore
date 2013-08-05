#!/usr/bin/env python2.7

import os
import logging
import sys, traceback
import multiprocessing


from experiment import Experiment
from analysis.packetdeliveryrateanalysis import PacketDeliveryRateAnalysis
from analysis.overheadanalysis import OverheadAnalysis
from analysis.delayanalysis import DelayAnalysis
from analysis.energydeadseriesanalysis import EnergyDeadSeriesAnalysis
from analysis.lastpacketanalysis import LastPacketAnalysis
from analysis.pathenergyanalysis import PathEnergyAnalysis

class ExperimentManagerWorker(multiprocessing.Process):

    def __init__(self, configuration, scenario_name, queue, is_verbose=False):
        super(ExperimentManagerWorker,self).__init__()
        self.simulations_directory = configuration['cwd']
        self.scenario_name = scenario_name
        self.verbose = is_verbose
        self.visualize = configuration['analysis_network']
        self.results_queue = queue
        self.routing_table_trace = configuration['analysis_routing_table_trace']
        self.logger = logging.getLogger('baltimore.experiment.ExperimentManagerWorker')
        self.logger.debug('creating an instance of ExperimentManagerWorker')
        self.csv = configuration['analysis_csv']
        self.logger.debug('will create csv files ' + str(self.csv))

        if configuration['analysis_location'] == "":
            self.location = self.simulations_directory
        else:
            self.location = configuration['analysis_location']


    def run(self):
        pid = os.getpid()

        try:
            self.logger.info('[%d] Scanning directory "%s" for simulation result files. This may take some time depending on the number of files...' %  (pid, self.simulations_directory))
            experiment = Experiment(self.simulations_directory + '/results', self.scenario_name, self.visualize, self.routing_table_trace, self.location)
            experiment_results = experiment.get_results()
            repetitions = experiment_results.get_number_of_repetitions()

            pdrAnalyser = PacketDeliveryRateAnalysis(self.scenario_name, self.location, repetitions, self.csv)
            pdrAnalyser.evaluate(experiment_results, self.verbose)

            overheadAnalyser = OverheadAnalysis(self.scenario_name, self.location, repetitions, self.csv)
            overheadAnalyser.evaluate(experiment_results, self.verbose)

            delayAnalyser = DelayAnalysis(self.scenario_name, self.location, repetitions, self.csv)
            delayAnalyser.evaluate(experiment_results, self.verbose)

            lastPacketAnalyser = LastPacketAnalysis(self.scenario_name, self.location, repetitions, self.csv)
            lastPacketAnalyser.evaluate(experiment_results, self.verbose)

            max_timestamp = lastPacketAnalyser.data_max

            energyDeadSeriesAnalyser = EnergyDeadSeriesAnalysis(self.scenario_name, self.location, max_timestamp, repetitions, self.csv)
            energyDeadSeriesAnalyser.evaluate(experiment_results, self.verbose)

            pathEnergyAnalyser = PathEnergyAnalysis(self.scenario_name, self.location, repetitions, self.csv)
            pathEnergyAnalyser.evaluate(experiment_results)

            result = (experiment, pdrAnalyser, lastPacketAnalyser, energyDeadSeriesAnalyser, delayAnalyser, pathEnergyAnalyser)

            self.logger.info("[%d] successfully read %d experiment(s) from %d scalar file(s)." % (pid, 1, experiment_results.get_number_of_repetitions()))
            self.results_queue.put(result)

        except Exception as exception:
            self.logger.error("[%d] an error occurred while evaluating experiment %s" % (pid, str(self.scenario_name) + " : " + str(exception)))
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
