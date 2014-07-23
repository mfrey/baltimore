#!/usr/bin/env python3

import sys
import math
import logging
import numpy as np

from .analysis import Analysis

class EnergyDeadSeriesAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "energy-dead-series", repetitions, csv)

        self.logger = logging.getLogger('baltimore.analysis.EnergyDeadSeriesAnalysis')
        self.logger.debug('creating an instance of EnergyDeadSeriesAnalysis for scenario %s', scenario)

        self.energy_dead_series = {}
        self.bin_size_in_seconds = 10


    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running energy dead series analysis")

        data = []

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("nodeEnergyDepletionTimestamp", repetition)

            for node in nodes:
                # get the timestamp and add +1 to the corresponding bin
                timestamp = experiment_results.repetitions[repetition].get_node_results()[node]["nodeEnergyDepletionTimestamp"]
                data.append([repetition, node, timestamp])

        self.max_time_stamp_value = np.amax([element[2] for element in data])
        self.nr_of_bins = int(self.max_time_stamp_value / self.bin_size_in_seconds) + 1

        repetitions = len(experiment_results.repetitions)
        # create all bins and initialize with zero and each bin is a list of dead notes per repetition
        global_bins = { key : [] for key in range(0, self.nr_of_bins) }

        data = []
        avg_timestamps = []
        median_timestamps = []
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("nodeEnergyDepletionTimestamp", repetition)
            bins_for_this_repetition = { key : 0 for key in range(0, self.nr_of_bins) }

            timestamps_of_repetition = []
            for node in nodes:
                # get the timestamp and add +1 to the corresponding bin
                timestamp = experiment_results.repetitions[repetition].get_node_results()[node]["nodeEnergyDepletionTimestamp"]
                timestamps_of_repetition.append(timestamp)
                data.append([repetition, node, timestamp])
                # in which interval does the timestamp lie?
                bin_nr = int(math.floor(timestamp / self.bin_size_in_seconds))
                bins_for_this_repetition[bin_nr] += 1

            # now save the bins to calculate the average later
            for bin_nr, value in list(bins_for_this_repetition.items()):
                global_bins[bin_nr].append(value)

            # save the average and median for the energy depletion timestamp
            avg_timestamps.append(np.average(timestamps_of_repetition))
            median_timestamps.append(np.median(timestamps_of_repetition))

        for bin_nr, value_list in list(global_bins.items()):
            # calculate the average number of dead notes from the corresponding bin of each repetition
            if value_list:
                average = np.average(value_list)
            else:
                average = 0

            self.energy_dead_series[bin_nr] = average

        avg_depletion_timestamp = np.average(avg_timestamps)
        median_depletion_timestamp = np.average(median_timestamps)
        self.logger.info("Average depletion timestamp: %f", avg_depletion_timestamp)
        self.logger.info("Median depletion timestamp : %f", median_depletion_timestamp)

        if self.draw:
            self._createplot()

        if self.csv:
            self.export_csv_raw(data)
            self.export_csv()


    def _create_plot(self):
        xdata = []
        ydata = []

        for bin_nr, value in list(self.energy_dead_series.items()):
            xdata.append(bin_nr * self.bin_size_in_seconds)
            ydata.append(value)

        ydata = np.cumsum(ydata)
        self.plot_barchart("Energy Dead Series", "Time [s]", "Dead Nodes", xdata, ydata)

    def export_csv(self):
        file_name = self.scenario + "_" + self.metric + ".csv"
        disclaimer = [['#'],
                      ['# ' + str(self.date) + ' - energy dead series for scenario ' + self.scenario],
                      ['# Aggregated over ' + str(self.repetitions) + ' repetitions'],
                      ['# Max time stamp was: ' + str(self.max_time_stamp_value)],
                      ['# The values are the average number of nodes that died in the time interval represented by the bin'],
                      ['#']]
        header = ['time', 'value']

        data =[]

        for bin_nr, value in list(self.energy_dead_series.items()):
            data.append([bin_nr*self.bin_size_in_seconds, value])

        self._write_csv_file(file_name, disclaimer, header, data)

    def export_csv_raw(self, data):
        file_name = self.scenario + "_" + self.metric + "_raw.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - energy dead series for scenario ' + self.scenario], ['#']]
        header = ['repetition', 'node', 'timestamp']

        self._write_csv_file(file_name, disclaimer, header, data)
