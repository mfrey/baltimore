#!/usr/bin/env python2.7

import sys
import logging
import os.path
import numpy as np

from .analysis import Analysis

from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class LastPacketAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "last_packet", repetitions, csv)

        self.logger = logging.getLogger('baltimore.analysis.LastPacketAnalysis')
        self.logger.debug('creating an instance of LastPacketAnalysis for scenario %s', scenario)

        self.data_min = -1
        self.data_max = -1
        self.data_median = -1
        self.data_std = -1
        self.data_avg = -1
        self.raw_data = {}

    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running arrival of last packet analysis")

        raw_data = [experiment_results.get_metric("timeOfLastReceivedPacket", repetition) for repetition in experiment_results.repetitions]

        # todo fix that
        for repetition in experiment_results.repetitions:
            if repetition not in self.raw_data:
                raw_data[repetition] = experiment_results.get_metric("timeOfLastReceivedPacket", repetition)

        data = [element for element in raw_data if element != 0]

        self.data_min = np.amin(data)
        self.data_max = np.amax(data)
        self.data_median = np.median(data)
        self.data_std = np.std(data)
        self.data_avg = np.average(data)

        self.logger.info("last packet: %d, %d, %d, %d, %d [min, max, median, std, avg] for scenario %s", self.data_min, self.data_max, self.data_median, self.data_std, self.data_avg, self.scenario)

        if self.draw:
            self.plot_boxplot("Arrival of Last Packet", "", "Arrival Time [ms]", data)

        if self.csv:
            self.export_csv()
            self.export_csv_raw()


    def export_csv(self):
        file_name = self.scenario + "_" + self.metric + "_aggregated.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - arrival of last packet for scenario ' + self.scenario],['# aggregated over ' + str(self.repetitions) + ' repetitions'],['#']]
        header = ['min', 'max', 'median', 'std', 'avg']
        data = [[self.data_min, self.data_max, self.data_median, self.data_std,  self.data_avg]]

        self._write_csv_file(file_name, disclaimer, header, data)

    def export_csv_raw(self):
        data = []
        file_name = self.scenario + "_" + self.metric + ".csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - arrival of last packet for scenario ' + self.scenario],['#']]
        header = ['repetition', 'time']

        for repetition, timestamp in self.raw_data.items():
            data.append([repetition, timestamp])

        self._write_csv_file(file_name, disclaimer, header, data)
