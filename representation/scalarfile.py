#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import shlex

from representation import node as n

class ScalarFile:

  def __init__(self, fileName):
    self.fileName = fileName
    self.file = open(fileName, "r")
    self.currentLineNr = 0
    self.nodes = {}
    
    print 'Parsing "%s"' % fileName
    
    self.read_preamble()
    self.read_body()
    
    self.file.close()

  def read_preamble(self):
    self.version = self.parse_key_value("version")
    self.run = self.parse_key_value("run")
    self.configname = self.parse_attribute("configname");
    self.datetime = self.parse_attribute("datetime");
    self.experiment = self.parse_attribute("experiment");
    self.inifile = self.parse_attribute("inifile");
    self.iterationvars = self.parse_attribute("iterationvars");
    self.iterationvars2 = self.parse_attribute("iterationvars2");
    self.measurement = self.parse_attribute("measurement");
    self.network = self.parse_attribute("network");
    self.processid = self.parse_attribute("processid");
    self.repetition = self.parse_attribute("repetition");
    self.replication = self.parse_attribute("replication");
    self.resultdir = self.parse_attribute("resultdir");
    self.runnumber = self.parse_attribute("runnumber");
    self.seedset = self.parse_attribute("seedset");
    
  def read_next_line(self):
    self.currentLineNr += 1
    return self.file.readline()
    
  def parse_key_value(self, key):
    words = self.file.readline().split(' ')
    if len(words) != 2:
      print "Could not parse key value line %d from %s because there are %d words" % (self.currentLineNr, self.fileName, len(words))
      raise
  
    if words[0] != key:
      print "Error while parsing key value line: Expected %s but got %s" % (key, words[0])
      raise
    
    return words[1].strip()

  def parse_attribute(self, name):
    words = self.read_next_line().split(' ')
    if len(words) != 3:
      print "Could not parse attribute line %d from %s because there are %d words" % (self.currentLineNr, self.fileName, len(words))
      raise
        
    if words[0] != 'attr' or words[1] != name:
      print "Could not parse line %d from %s for attribute %s" % (self.currentLineNr, self.fileName, name)
      raise
    
    return words[2].strip()

  def read_body(self):
    line = self.read_next_line()
    while line:
        line = self.read_next_line()
        self.parse(line)

  def parse(self, line):
    if line.startswith('scalar'):
       self.handle_scalar(line)
    # else ignore this line for now

  def handle_scalar(self, line):
	identifier = self.get_node_identifier(line)

	if identifier not in self.nodes:
	  self.nodes[identifier] = n.Node()
	  self.nodes[identifier].identifier = identifier

	key, value = shlex.split(line)[2], shlex.split(line)[3]
	self.nodes[identifier].results[key] = value

  def get_node_identifier(self, line):
    # TODO: fix that (that's quite aweful)
    return line.split(' ')[1].split('.')[1].split('[')[1].split(']')[0]
