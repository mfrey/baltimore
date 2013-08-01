#!/usr/bin/env python2.7

import sys
import math
import logging
import numpy as np

from analysis import Analysis

class EnergyDeadSeriesAnalysis(Analysis):
    def __init__(self, scenario, location, timestamp, repetitions, csv):
        Analysis.__init__(self, scenario, location, "energy-dead-series", repetitions, csv)

        self.logger = logging.getLogger('baltimore.analysis.EnergyDeadSeriesAnalysis')
        self.logger.debug('creating an instance of EnergyDeadSeriesAnalysis for scenario %s', scenario)
        
        self.energy_dead_series = {}
        # TODO: should this value somehow be computed?
        self.bin_size_in_seconds = 10
        # the max timestamp value is passed to the analysis via the last received packet analysis
        self.max_time_stamp_value = timestamp 
        # TODO: check if this is a issue 
        self.nr_of_bins = int(self.max_time_stamp_value / self.bin_size_in_seconds)

    def evaluate(self, experiment_results, is_verbose=False):
        repetitions = len(experiment_results.repetitions)

        self.logger.info("running energy dead series analysis")

        # create all bins and initialize with zero
        global_bins = {}
        for i in range(0, self.nr_of_bins-1):
            # each bin is a list of dead notes per repetition 
            global_bins[i] = []
        
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("nodeEnergyDepletionTimestamp")
            bins_for_this_repetition = {}
            for i in range(0, self.nr_of_bins-1):
                bins_for_this_repetition[i] = 0
            
            for node in nodes:
                # get the timestamp and add +1 to the corresponding bin
                timestamp = experiment_results.repetitions[repetition].get_node_results()[node]["nodeEnergyDepletionTimestamp"]
                # in which interval does the timestamp lie?
                bin_nr = int(math.floor(timestamp / self.bin_size_in_seconds))
                bins_for_this_repetition[bin_nr] += 1
                
            # now save the bins to calculate the average later
            for bin_nr, value in bins_for_this_repetition.iteritems(): 
                global_bins[bin_nr].append(value)

        for bin_nr, value in global_bins.iteritems():
            # calculate the average number of dead notes from the corresponding bin of each repetition
            if value:
                average = np.average(value)
            else:
                average = 0

            self.energy_dead_series[bin_nr] = average
                
        self._create_plot()

    def _create_plot(self):
        xdata = []
        ydata = []
        
        nr_of_bars = 0
        for bin_nr, value in self.energy_dead_series.iteritems():
            xdata.append(bin_nr * self.bin_size_in_seconds)
            ydata.append(value)
            if value > 0:
                nr_of_bars += 1
 
        ydata = np.cumsum(ydata)
        width = self.max_time_stamp_value / nr_of_bars
        self.plot_barchart("Energy Dead Series", "Time [s]", "Dead Nodes", xdata, ydata, width)
