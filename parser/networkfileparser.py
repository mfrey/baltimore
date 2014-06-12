#!/usr/bin/env python3

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
        nodes = self.network.nodes()
        positions = nx.get_node_attributes(self.network,'pos')
        radius = nx.get_node_attributes(self.network,'radius')

        while nodes:
            u = nodes.pop()
            pu = positions[u]
            for v in nodes:
                pv = positions[v]
                d = sum(((a-b)**2 for a,b in zip(pu,pv)))
                if d <= radius[u]**2:
                    self.network.add_edge(u,v)
