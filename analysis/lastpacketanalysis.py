#!/usr/bin/env python2.7

import sys
import os.path
import numpy as np

from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class LastPacketAnalysis:
    def __init__(self, scenario, location):
        self.data = []
        self.scenario = scenario
        self.location = location

    def evaluate(self, experiment_results, is_verbose=False):
        print "\nRunning arrival of last packet analysis.."
        raw_data = [experiment_results.get_metric("timeOfLastReceivedPacket", repetition) for repetition in experiment_results.repetitions]
        self.data = [element for element in raw_data if element != 0]
        self._create_boxplot()
        

    def _create_boxplot(self):
        plot = BoxPlot()
        plot.title = "Arrival of Last Packet"
        plot.xlabel = ""
        plot.ylabel = "Arrival Time [ms]"
        plot.draw(self.data, os.path.join(self.location, self.scenario + "_last_packet.png"))



    
