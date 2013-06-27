#!/usr/bin/env python2.7

import os.path

from plot.lineplot import LinePlot

class Analysis:
    def __init__(self, scenario, location, metric):
        self.scenario = scenario
        self.location = location
        self.metric = metric

    def plot_lineplot(self, title, xlabel, ylabel, xdata, ydata):
        plot = LinePlot()

        plot.title = title
        plot.xlabel = xlabel
        plot.ylabel = ylabel

        plot.draw(xdata, ydata, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))

