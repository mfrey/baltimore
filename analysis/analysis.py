#!/usr/bin/env python2.7


import os.path
import logging

from plot.boxplot import BoxPlot
from plot.lineplot import LinePlot
from plot.barchart import BarChart

class Analysis:
    def __init__(self, scenario, location, metric):
        self.scenario = scenario
        self.location = location
        self.metric = metric
        self.logger = logging.getLogger('baltimore.analysis.Analysis')

    def plot_lineplot(self, title, x_label, y_label, x_data, y_data):
        plot = LinePlot()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.draw(x_data, y_data, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))

    def plot_boxplot(self, title, x_label, y_label, data):
        plot = BoxPlot()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.draw(data, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))
    
    def plot_barchart(self, title, x_label, y_label, x_data, y_data, bar_widths=-1):
        plot = BarChart()
        plot.title = title
        plot.xlabel = x_label
        plot.ylabel = y_label
        plot.bar_widths = bar_widths
        plot.draw(x_data, y_data, os.path.join(self.location, self.scenario + "_" + self.metric + ".png"))
        
    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d        

    def __setstate__(self, d):
        self.__dict__.update(d)