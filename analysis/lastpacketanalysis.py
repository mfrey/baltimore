#!/usr/bin/env python2.7

import sys
import os.path
import numpy as np

from analysis import Analysis

from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class LastPacketAnalysis(Analysis):
    def __init__(self, scenario, location):
        Analysis.__init__(self, scenario, location, "last_packet")
        self.data_min = -1
        self.data_max = -1
        self.data_median = -1
        self.data_std = -1
        self.data_avg = -1

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning arrival of last packet analysis.."
        raw_data = [experiment_results.get_metric("timeOfLastReceivedPacket", repetition) for repetition in experiment_results.repetitions]
        data = [element for element in raw_data if element != 0]

        self.data_min = np.amin(result)
        self.data_max = np.amax(result)
        self.data_median = np.median(result)
        self.data_std = np.std(result)
        self.data_avg = np.average(result)

        self.plot_boxplot("Arrival of Last Packet", "", "Arrival Time [ms]", data)
