#!/usr/bin/env python2.7

import re
import shlex

from representation import node as n

class ScalarFile:
  def __init__(self):
    self.version = -1
    self.run = "Scenario05-0-20130429-11:11:04-21740"
    self.configname = "uninitialized configuration name"
    self.datetime = "20130429-11:11:04"
    self.experiment = "uninitialized experiment" 
    self.inifile = "no ini file set" 
    self.measurement = ""
    self.network = "uninitialized network name"
    self.processid = -1
    self.repetition = -1
    self.replication = "uninitialized"
    self.resultdir = "uninitialized"
    self.runnumber = -1
    self.seedset = -1
    self.nodes = {}

  def read(self, filename):
    result_arr = []
    with open(filename, "r") as f:
      # handle the preamble of the scalar file
#      preamble = f.readlines()[:16]
 #     self.handle_preamble(preamble)

      for _ in xrange(18):
        next(f)

      for line in f:
        self.handle_line(line)
      

  def get_node_identifier(self, line):
    # TODO: fix that (that's quite aweful)
    return line.split(' ')[1].split('.')[1].split('[')[1].split(']')[0]

  def handle_line(self, line):
    if line.startswith('scalar'):
       self.handle_scalar(line)
#     elif line.startswith('field'):
#       self.handle_field(line)
#     elif line.startswith('bin'):
#       self.handle_bin(line)
#     elif line.startswith('attr'):
#       self.handle_attr(line)
    #else:
      #raise "unkown entry type in scalar file"

#  def handle_field(self, line):
#    raise NotImplemented, "method not implemented"

#  def handle_bin(self, line):
#    raise NotImplemented, "method not implemented"

  def handle_scalar(self, line):
	identifier = self.get_node_identifier(line)

	if identifier not in self.nodes:
	  self.nodes[identifier] = n.Node()
	  self.nodes[identifier].identifier = identifier

	key, value = shlex.split(line)[2], shlex.split(line)[3]
	self.nodes[identifier].results[key] = value

#  def handle_bin(self, attr):
#    raise NotImplemented, "method not implemented"

  def handle_preamble(self, preamble):
    # remove the new lines from the entries
    preamble = map(lambda s: s.strip(), preamble)

    # parse the preamble array
    version = preamble[0].split(' ')[1] 
    configname = preamble[2].split(' ')[2]
    # datetime = ...
    experiment = preamble[4].split(' ')[2]
    inifile = preamble[5].split(' ')[2]
    network = preamble[9].split(' ')[2]
    processid = preamble[10].split(' ')[2]
    repetition = preamble[11].split(' ')[2]
    # replication = preamble[5].split(' ')[2]
    resultdir = preamble[13].split(' ')[2]
    runnumber = preamble[14].split(' ')[2]

  def handle_node(self, node):
     print "not implemented"
