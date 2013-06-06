#!/usr/bin/env python2.7

import shlex

from omnetfileparser import OMNeTFileParser

#from experiment.repetitiondata import RepetitionData

class VectorFileParser(OMNeTFileParser):
    def __init__(self, file_name):
        OMNeTFileParser.__init__(self, file_name)

    def read(self, file_path):
        try:
            self.file_path = file_path
            self.current_line_nr = 0
#            self.file_name = open(self.file_path, "r")
            
#            parameters = self._read_preamble()
            nodes = self._read_body()
            
#            return RepetitionData(parameters, nodes)
        
        except IOError: 
            print "Error: can\'t find file ", self.file_path, " or read it" 
        finally: 
            self.file.close()

    def _read_body(self):
        nodes = {}
        line = self._read_next_line()
        while line:
            line = self._read_next_line()
            self._parse(line, nodes)
            
        return nodes
    
    def _parse(self, line, nodes):
        if line.startswith('scalar'):
            node_identifier = self._get_node_identifier(line)
            
            if node_identifier not in nodes:
                nodes[node_identifier] = {}
            
            metric_name, value = shlex.split(line)[2], shlex.split(line)[3]
            nodes[node_identifier][metric_name] = float(value)

if __name__ == "__main__":
    parser = VectorFileParser("/home/frey/Desktop/Projekte/code/ara-sim/simulations/ara/results/ARATEST-0.sca")
