#!/usr/bin/env python2.7

from math import pow, sqrt
import networkx as nx

class NetworkFileParser:
    def __init__(self):
        self.network = nx.Graph()

    def read(self, file_path):
        with open(file_path) as f:
            for line in f:
                self._parse_line(line)

        self._create_connections()
   
    def _parse_line(self, line):
        entry = line.strip().split()
        self._create_node(entry[0], float(entry[1]), float(entry[2]), float(entry[3]))

    def _create_node(self, node_identifier, x_position, y_position, node_radius):
        self.network.add_node(node_identifier, pos=(x_position, y_position),radius=node_radius)

    def _create_connections(self):
        positions = nx.get_node_attributes(self.network, 'pos')
        radius = nx.get_node_attributes(self.network, 'radius')

        for current_node in self.network.nodes():
            current_node_x = positions[current_node][0]
            current_node_y = positions[current_node][1]
            current_node_radius = radius[current_node]

            for next_node in self.network.nodes():
                if current_node != next_node:
                    next_node_x = positions[next_node][0]
                    next_node_y = positions[next_node][1]

                    distance = sqrt(pow(current_node_x - next_node_x, 2) + pow(current_node_x - next_node_x, 2))

                    if distance <= current_node_radius:
                        self.network.add_edge(current_node, next_node)
                
