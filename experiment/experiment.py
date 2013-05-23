#!/usr/bin/env python2.7

import os
import sys

import matplotlib
matplotlib.use("Agg")

from networkx import networkx as nx
from matplotlib import pyplot as plt
from fnmatch import fnmatch as file_name_match

from parser.scalarfileparser import ScalarFileParser
from parser.networkfileparser import NetworkFileParser
from experimentresult import ExperimentResult 

class Experiment:
    def __init__(self, directory, scenario_name, visualize):
        self.directory = directory
        self.scenario_name = scenario_name
        self.visualize = visualize
    
    def get_results(self):
        print "Reading results of experiment [%s]" % self.scenario_name
        scalar_parser = ScalarFileParser()
        experiment_results = ExperimentResult()
        
        for file_name in os.listdir(self.directory):
            file_path = self.directory + '/' + file_name
            if file_name_match(file_name, self.scenario_name + '*.sca'):
                result = scalar_parser.read(file_path)
                experiment_results.add_repetition(result)
                self.print_progress()
            elif file_name_match(file_name, self.scenario_name + '*.net'):
                if self.visualize:
                    network_file_parser = NetworkFileParser()
                    network_file_parser.read(file_path)

                    positions = nx.get_node_attributes(network_file_parser.network,'pos')
                    nx.draw(network_file_parser.network, positions, node_color="#99CC00")
                    plt.savefig(self.directory + '/' + self.scenario_name + '_network.png')

        print
        return experiment_results

    def print_progress(self):
        sys.stdout.write(".")
        sys.stdout.flush()
