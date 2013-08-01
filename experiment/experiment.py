#!/usr/bin/env python2.7

import sys

from networkx import networkx as nx
from matplotlib import pyplot as plt
from fnmatch import fnmatch as file_name_match
from os.path import basename
from os import listdir

from parser.scalarfileparser import ScalarFileParser
from parser.vectorfileparser import VectorFileParser
from parser.networkfileparser import NetworkFileParser
from parser.routingtabledataparser import RoutingTableDataParser
from parser.mobilitydataparser import MobilityDataParser
from experimentresult import ExperimentResult
from plot.routingtableplot import RoutingTablePlot

class Experiment:
    def __init__(self, results_directory, scenario_name, visualize, routing_table_trace, location):
        self.results_directory = results_directory
        self.scenario_name = scenario_name
        self.enable_network_visualize = visualize
        self.enable_routing_table_trace = routing_table_trace
        self.location = location

    def get_results(self):
        print "Reading results of experiment [%s]" % self.scenario_name
        experiment_results = ExperimentResult()

        for filename in listdir(self.results_directory):
            file_path = self.results_directory + '/' + filename
            if file_name_match(filename, self.scenario_name + '-' + '*.sca'):
                result = self._parse_scalar_file(file_path)
                experiment_results.add_repetition(result)
            elif file_name_match(filename, self.scenario_name + '-'+'*.vec'):
                result = self._parse_vector_file(file_path)
                experiment_results.add_repetition(result)
            elif file_name_match(filename, self.scenario_name + '-'+'*.rtd'):
                if self.enable_routing_table_trace:
                    self._generate_routing_table_plots("192.168.0.2", filename) #FIXME: make the destination a parameter
                    self.print_progress()
            elif file_name_match(filename, self.scenario_name + '-'+'*.mtr'):
                parser = MobilityDataParser()
                data = parser.read(self.results_directory + "/" + filename)
            elif file_name_match(filename, self.scenario_name + '-' + '*.net'):
                if self.enable_network_visualize:
                    self._generate_network_plots(file_path)

        return experiment_results


    def _parse_scalar_file(self, file_name):
        scalar_parser = ScalarFileParser(file_name)
        result = scalar_parser.read()
        self.print_progress()
        return result

    def _parse_vector_file(self, file_name):
        vector_parser = VectorFileParser(file_name)
        result = vector_parser.read()
        self.print_progress()
        return result

    def _generate_routing_table_plots(self, target, file_name):
        parser = RoutingTableDataParser()
        data = parser.read_data_from(self.results_directory + "/" + file_name, target)
        plot = RoutingTablePlot()
        plot_filename = self.location + "/" + file_name + '.png'
        plot.draw(data, plot_filename)

    def _generate_network_plots(self, file_name):
        parser = NetworkFileParser()
        parser.read(file_name)
        positions = nx.get_node_attributes(parser.network,'pos')
        nx.draw(parser.network, positions, node_color="#99CC00")
        plt.savefig(self.location + '/' + self.scenario_name + '_network.png')
        plt.close()

    def print_progress(self):
        sys.stdout.write(".")
        sys.stdout.flush()
