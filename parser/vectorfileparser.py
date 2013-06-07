#!/usr/bin/env python2.7

import shlex

from omnetfileparser import OMNeTFileParser
from experiment.repetitiondata import RepetitionData

class VectorFileParser(OMNeTFileParser):
    def __init__(self, file_name):
        OMNeTFileParser.__init__(self, file_name)
        self.vector_settings = {}
        self.vector_dict = {}
        self.nodes = {}

    def read(self):
        try:
            nodes = self._read_body()
            self._build_result_dict()
            return RepetitionData(parameters, nodes)
        except IOError: 
            print "Error: can\'t find file ", self.file_path, " or read it" 
        finally: 
            self.file_handle.close()

    def _build_result_dict(self):
        for key, value in self.vector_dict.items():
            node_identifier, metric = self.vector_settings[key][0], self.vector_settings[key][1]
            self.nodes[node_identifier][metric] = value

    def _read_body(self):
        line = self._read_next_line()
        while line:
            line = self._read_next_line()
            self._parse(line)
    
    def _parse(self, line):
        line = " ".join(line.split())

        if line.startswith('vector'):
            vector_preamble = self._parse_vector_preamble(line)
            node_identifier = self._get_node_identifier(line)

            if node_identifier not in self.nodes:
                self.nodes[node_identifier] = {}
            
            self.nodes[str(node_identifier)][vector_preamble[2]] = []
        elif len(line) > 0 and line[0].isdigit():
            self._parse_vector_line(line)

    
    def _parse_vector_preamble(self, line):
        content = line.split(' ')
        vector_identifier, node, vector_type = content[1], content[2], content[3]
        column_spec = ""

        # the columSpec attribute is set
        if len(content) > 4:
            column_spec = content[4]

        if vector_identifier not in self.vector_dict:
            # holds the values of the vector 
            self.vector_dict[vector_identifier] = []
            # denotes the type of the vector and the node it belongs to
            self.vector_settings[vector_identifier] = [self._get_node_identifier(node), vector_type]

        return (vector_identifier, node, vector_type)

    def _parse_vector_line(self, line):
        content = line.split(' ')
        vector_identifier, value = content[0], content[3]
        self.vector_dict[vector_identifier].append(value)
