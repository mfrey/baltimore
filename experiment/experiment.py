#!/usr/bin/env python2.7

import sys

from networkx import networkx as nx
from matplotlib import pyplot as plt
from fnmatch import fnmatch as file_name_match
from os.path import basename
from os import listdir

from parser.scalarfileparser import ScalarFileParser
from parser.networkfileparser import NetworkFileParser
from parser.routingtabledataparser import RoutingTableDataParser
from experimentresult import ExperimentResult
from plot.routingtableplot import RoutingTablePlot

class Experiment:
    def __init__(self, results_directory, scenario_name, visualize):
        self.results_directory = results_directory
        self.scenario_name = scenario_name
        self.visualize = visualize
    
    def get_results(self):
        print "Reading results of experiment [%s]" % self.scenario_name
        scalar_parser = ScalarFileParser()
        experiment_results = ExperimentResult()
        
        for filename in listdir(self.results_directory):
            file_path = self.results_directory + '/' + filename
            if file_name_match(filename, self.scenario_name + '-' + '*.sca'):
                result = scalar_parser.read(file_path)
                experiment_results.add_repetition(result)
                self.print_progress()
            elif file_name_match(filename, self.scenario_name + '-'+'*.rtd'):
                parser = RoutingTableDataParser()
                data = parser.read_data_from(self.results_directory + "/" + filename, "192.168.0.2") #FIXME make the destination a parameter
                plot = RoutingTablePlot()
                plot_filename = self.results_directory + "/" + filename + '.png' 
                plot.draw(data, plot_filename)
                self.print_progress()
            elif file_name_match(filename, self.scenario_name + '-' + '*.net'):
                if self.visualize:
                    network_file_parser = NetworkFileParser()
                    network_file_parser.read(file_path)

                    positions = nx.get_node_attributes(network_file_parser.network,'pos')
                    nx.draw(network_file_parser.network, positions, node_color="#99CC00")
                    plt.savefig(self.results_directory + '/' + self.scenario_name + '_network.png')

        print
        return experiment_results

    def print_progress(self):
        sys.stdout.write(".")
        sys.stdout.flush()
