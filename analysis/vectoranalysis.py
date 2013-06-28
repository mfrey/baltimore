#!/usr/bin/env python2.7

import os.path

from analysis import Analysis
from plot.boxplot import BoxPlot

class VectorAnalysis(Analysis):
    def __init__(self, scenario, location, metric):
        Analysis.__init__(self, scenario, location, metric)


