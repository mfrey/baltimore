#!/usr/bin/env python2.7

import os.path

from analysis import Analysis
from plot.boxplot import BoxPlot

class VectorAnalysis(Analysis):
    def __init__(self, scenario, location, metric):
        Analysis.__init__(self, scenario, location, metric)


    def plot_boxplot(self, title, x_label, y_label, data):
        plot = BoxPlot()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.draw(data, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))
