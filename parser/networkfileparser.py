#!/usr/bin/env python2.7

import networkx as nx

class NetworkFileParser:
    def __init__(self):
        self.network = nx.Graph()

    def read(self, file_path):
        with open(file_path) as f:
            for line in f:
                self._parse_line(line)
   
    def _parse_line(self, line):
        entry = line.strip().split()
        self._create_node(entry[0], entry[1], entry[2])

    def _create_node(self, node_identifier, x_position, y_position):
        self.network.add_node(node_identifier, pos=(x_position, y_position))
