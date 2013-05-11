#!/usr/bin/env python2.7

import shlex
from experiment.repetitiondata import RepetitionData

class ScalarFileParser:
    def read(self, file_path):
        try:
            self.file_path = file_path
            self.current_line_nr = 0
            self.file = open(self.file_path, "r")
            
            parameters = self._read_preamble()
            nodes = self._read_body()
            
            return RepetitionData(parameters, nodes)
        
        except IOError: 
            print "Error: can\'t find file ", self.file_path, " or read it" 
        finally: 
            self.file.close()
    
    def _read_preamble(self):
        return {'version': self._parse_key_value("version"),
                'run': self._parse_key_value("run"),
                'configname': self._parse_attribute("configname"),
                'datetime': self._parse_attribute("datetime"),
                'experiment': self._parse_attribute("experiment"),
                'inifile': self._parse_attribute("inifile"),
                'iterationvars': self._parse_attribute("iterationvars"),
                'iterationvars2': self._parse_attribute("iterationvars2"),
                'measurement': self._parse_attribute("measurement"),
                'network': self._parse_attribute("network"),
                'processid': self._parse_attribute("processid"),
                'repetition': self._parse_attribute("repetition"),
                'replication': self._parse_attribute("replication"),
                'resultdir': self._parse_attribute("resultdir"),
                'runnumber': self._parse_attribute("runnumber"),
                'seedset': self._parse_attribute("seedset")}
    
    def _parse_key_value(self, key):
        words = self.file.readline().split(' ')
        if len(words) != 2:
            print "Could not parse key value line %d from %s because there are %d words" % (self.current_line_nr, self.file_path, len(words))
            raise
        
        if words[0] != key:
            print "Error while parsing key value line: Expected %s but got %s" % (key, words[0])
            raise
        
        return words[1].strip()
    
    def _parse_attribute(self, name):
        words = self._read_next_line().split(' ')
        if len(words) != 3:
            print "Could not parse attribute line %d from %s because there are %d words" % (self.current_line_nr, self.file_path, len(words))
            raise
            
        if words[0] != 'attr' or words[1] != name:
            print "Could not parse line %d from %s for attribute %s" % (self.current_line_nr, self.file_path, name)
            raise
        
        return words[2].strip()
    
    def _read_body(self):
        nodes = {}
        line = self._read_next_line()
        while line:
            line = self._read_next_line()
            self._parse(line, nodes)
            
        return nodes
    
    def _read_next_line(self):
        self.current_line_nr += 1
        return self.file.readline()
    
    def _parse(self, line, nodes):
        if line.startswith('scalar'):
            node_identifier = self._get_node_identifier(line)
            
            if node_identifier not in nodes:
                nodes[node_identifier] = {}
            
            metric_name, value = shlex.split(line)[2], shlex.split(line)[3]
            nodes[node_identifier][metric_name] = float(value)
    
    def _get_node_identifier(self, line):
        # TODO: fix that (that's quite aweful)
        return line.split(' ')[1].split('.')[1].split('[')[1].split(']')[0]