#!/usr/bin/env python2.7

import networkx as nx

class NetworkFileParser:
    def __init__(self):
        self.network = nx.Graph()

    def read(self, file_path):
        try:
            self.file_path = file_path
            self.file = open(self.file_path, "r")
            for line in self.file:
                self._parse_line(line)
        
        except IOError: 
            print "Error: can\'t find file ", self.file_path, " or read it" 
        finally: 
            self.file.close()
   
    def _parse_line(self, line):
        entry = line.strip().split()
        node = entry[0]
        x_position = entry[1]
        y_position = entry[2]
        self._create_node(node, x_position, y_position)


    def _create_node(self, node_identifier, x_position, y_position):
        self.network.add_node(node_identifier, pos=(x_position, y_position))

