#!/usr/bin/env python3

import sys
import math
import logging
import numpy as np
import pprint

from .analysis import Analysis

class ResidualEnergyAnalysis(Analysis):
    def __init__(self, scenario, location, max_timestamp, repetitions, csv):
        Analysis.__init__(self, scenario, location, "residual-energy", repetitions, csv)
        self.logger = logging.getLogger('baltimore.analysis.ResidualAnalysis')

        self.bin_size_in_seconds = 10
        max_timestamp = 900
        self.nr_of_bins = int(max_timestamp / self.bin_size_in_seconds) + 1

    def evaluate(self, experiment_results, is_verbose=False):
        self.logger.info("running residual energy analysis")

        metric_name = 'energyLevel'

        # create all bins and initialize with an empty list
        # each bin is a list of residual energy values for the corresponding time interval
        global_bins = { bin_nr : [] for bin_nr in range(0, self.nr_of_bins) }
        self.avg_residual_energy_values = []
        highest_energy_capacity = self._find_highest_energy_capacity(experiment_results, metric_name)

        for repetition_nr in experiment_results:
            bins_for_this_repetition = { bin_nr : [] for bin_nr in range(0, self.nr_of_bins) }
            nodes = experiment_results.nodes_have_metric(metric_name, repetition_nr)

            # sort the residual energy values in the bins for this repetition
            for node_nr in nodes:
                time_value_tuples = experiment_results.get_tuple_metric_per_node(metric_name, node_nr, repetition_nr)

                for time_value_tuple in time_value_tuples:
                    timestamp = float(time_value_tuple[0])
                    residual_energy =  time_value_tuple[1]

                    bin_nr = int(math.floor(timestamp / self.bin_size_in_seconds))
                    bins_for_this_repetition[bin_nr].append(residual_energy)

            # calculate the average residual energy values and sort these in the global bins
            for bin_nr, residual_energy_values in bins_for_this_repetition.items():
                if residual_energy_values:
                    avg_residual_energy = np.average(residual_energy_values)
                    global_bins[bin_nr].append(avg_residual_energy)

        for bin_nr, avg_residual_energy_values in global_bins.items():
            if avg_residual_energy_values:
                global_avg_residual_energy = np.average(avg_residual_energy_values)
                global_avg_residual_energy_percent = global_avg_residual_energy * 100 / highest_energy_capacity
                time_interval_start = int(bin_nr*self.bin_size_in_seconds)
                self.avg_residual_energy_values.append([time_interval_start, global_avg_residual_energy_percent])

        if self.csv:
            self.export_csv(highest_energy_capacity)

    def _find_highest_energy_capacity(self, experiment_results, metric_name):
        highest_capacity = 0
        nodes = experiment_results.nodes_have_metric(metric_name)
        for node_nr in nodes:
            time_value_tuples = experiment_results.get_tuple_metric_per_node(metric_name, node_nr, 0)

            for time_value_tuple in time_value_tuples:
                timestamp = float(time_value_tuple[0])
                residual_energy =  time_value_tuple[1]

                if residual_energy > highest_capacity:
                    highest_capacity = residual_energy

        return highest_capacity

    def export_csv(self, highest_energy_capacity):
        file_name = self.scenario + "_" + self.metric + ".csv"
        comment = [['#'],
                   ['# ' + str(self.date) + ' - residual energy averages for scenario ' + self.scenario],
                   ['# Averaged over ' + str(self.repetitions) + ' repetitions'],
                   ['#']]

        header = ['time', 'value']

        self._write_csv_file(file_name, comment, header, self.avg_residual_energy_values)
