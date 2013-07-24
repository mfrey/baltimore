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

        if configuration['analysis_location'] == "":
            self.location = self.simulations_directory
        else:
            self.location = configuration['analysis_location']

    def run(self):
        pid = os.getpid()
        try:
            # TODO: change this to logging, so we only print it if required
            self.logger.info('[%d] Scanning directory "%s" for simulation result files. This may take some time depending on the number of files...' %  (pid, self.simulations_directory))
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

            energyDeadSeriesAnalyser = EnergyDeadSeriesAnalysis(self.scenario_name, self.location)
            energyDeadSeriesAnalyser.evaluate(experiment_results, self.verbose)

            lastPacketAnalyser = LastPacketAnalysis(self.scenario_name, self.location)
            lastPacketAnalyser.evaluate(experiment_results, self.verbose)

#            pathEnergyAnalyser = PathEnergyAnalysis(self.scenario_name, self.location)
#            pathEnergyAnalyser.evaluate(experiment_results, self.verbose)
#            pathEnergyAnalyser.evaluate_different(experiment_results)

            # TODO: change this to logging, so we only print it if required
            nr_of_parsed_files = experiment_results.get_number_of_repetitions()
            self.logger.info("[%d] successfully read %d experiment(s) from %d scalar file(s)." % (pid, 1, nr_of_parsed_files))
           
#            result = (experiment, pdrAnalyser, lastPacketAnalyser, energyDeadSeriesAnalyser)
#            result = (experiment, pdrAnalyser, lastPacketAnalyser, energyDeadSeriesAnalyser, delayAnalyser)
            result = (experiment, delayAnalyser)
            self.results_queue.put(result)

        except Exception as exception:
            self.logger.error("[%d] an error occurred while evaluating experiment %s" % (pid, str(self.scenario_name) + " : " + str(exception)))
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
