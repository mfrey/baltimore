#!/usr/bin/env python2.7

import sys
import os.path
import logging
import traceback

import numpy as np

import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

from collections import OrderedDict

from analysis import Analysis
from pathenergy import PathEnergy

from plot.lineplot import LinePlot
from plot.boxplot import BoxPlot

class PathEnergyAnalysis(Analysis):
    def __init__(self, scenario, location, repetitions, csv):
        Analysis.__init__(self, scenario, location, "path-energy", repetitions, csv)
        self.logger = logging.getLogger('baltimore.analysis.PathEnergyAnalysis')
        self.logger.debug('creating an instance of PathEnergyAnalysis for scenario %s', scenario)
        self.path_energy = {}
        self.path_energy_temp = {}


    def evaluate(self, experiment_results):
        self.logger.debug('running PathEnergyAnalysis for scenario %s', self.scenario)
        raw_data = []

        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("routeEnergy")
            for node in nodes:
                data = experiment_results.get_tuple_metric_per_node("routeEnergy", node, repetition)

                for element in data:
                    raw_data.append([repetition, node, float(element[0]), float(element[1])])

        if self.csv:
            self.logger.debug('write PathEnergyAnalysis csv file for scenario %s', self.scenario)
            self._export_csv_raw(raw_data)

        if self.draw:
            self._plot_path_energy(experiment_results)

    # FIXME
    def _plot_path_energy(self, experiment_results):
        Tmax = 6000
        for repetition in experiment_results:
            nodes = experiment_results.nodes_have_metric("routeEnergy")
            for node in nodes:
                data = experiment_results.get_tuple_metric_per_node("routeEnergy", node, repetition)

                for element in data:
                    raw_data.append([repetition, node, float(element[0]), float(element[1])])

                T = [float(pair[0]) for pair in data]
                R = [float(pair[1]) for pair in data]
                bw = 0.5

                trange = [0, Tmax]
                bins = 5000

                dx = (trange[1] - trange[0]) / bins

                # compute sum_i K(x - x_i) y_i
                hist_R, edges = np.histogram(T, range=trange, bins=bins, weights=R)
                kde_R = gaussian_filter(hist_R, bw / dx)

                # compute sum_i K(x - x_i)
                hist_T, edges = np.histogram(T, range=trange, bins=bins)
                kde_T = gaussian_filter(hist_T, bw / dx)

                # compute the Nadaraya-Watson estimate
                interpolated_R = kde_R / kde_T

                # computer x-axis
                domain = (edges[1:] + edges[:-1]) / 2.0

                if self.draw:
                    plt.plot(domain, interpolated_R)
                    file_name = "alternative_path-energy_node-" + str(node)
                    plt.savefig(os.path.join(self.location, self.scenario + "_" + file_name + ".png"))
                    plt.close()



    def _export_csv_raw(self, data):
        file_name = self.scenario + "_" + self.metric + "raw.csv"
        disclaimer = [['#'],['#'], ['# ' + str(self.date) + ' - path energy for scenario ' + self.scenario + ' per repetition'],['#'],['#']]
        header = ['repetition', 'node', 'timestamp', 'energy']

        self._write_csv_file(file_name, disclaimer, header, data)
