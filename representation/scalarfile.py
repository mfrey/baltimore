#!/usr/bin/env python2.7

import re

from representation import node as n

class ScalarFile:
  def __init__(self):
    version = -1
    run = "Scenario05-0-20130429-11:11:04-21740"
    configname = "uninitialized configuration name"
    datetime = "20130429-11:11:04"
    experiment = "uninitialized experiment" 
    inifile = "no ini file set" 
    measurement = ""
    network = "uninitialized network name"
    processid = -1
    repetition = -1
    replication = "uninitialized"
    resultdir = "uninitialized"
    runnumber = -1
    seedset = -1

  def read(self, filename):
    result_arr = []
    with open(filename, "r") as f:
      # handle the preamble of the scalar file
#      preamble = f.readlines()[:16]
 #     self.handle_preamble(preamble)

      for _ in xrange(18):
        next(f)
      
      nodes = {}
      nodes[0] = n.Node()
      nodes[0].identifier = 0

      for line in f:
        if not line.startswith('attr'): 
          # determine the node id
          identifier = self.get_node_identifier(line)
          if identifier != -1:
            # check if the node id has already been seen and stored
            if identifier in nodes:
              size = len(line.split(' '))
              key, value = line.split(' ')[size-2], line.split(' ')[size-1]
              print value
              #nodes[identifier]
            # create a new node
            else:
              nodes[identifier] = n.Node()
              nodes[identifier].identifier = identifier
          # add the content
         # print line

      print nodes
      

  def get_node_identifier(self, line):
    if not line.startswith('field'):
      if not line.startswith('bin'):
    # TODO: fix that (that's quite aweful)
        return line.split(' ')[1].split('.')[1].split('[')[1].split(']')[0]
    else:
      return -1

  def handle_line(self, line):
     if line.startswith('scalar'):
       self.handle_scalar(line)
     elif line.startswith('field'):
       self.handle_field(line)
     elif line.startswith('bin'):
       self.handle_bin(line)
     elif line.startswith('attr'):
       self.handle_attr(line)
     else:
       raise "unkown entry type in scalar file"

  def handle_field(self, line):
     raise NotImplemented, "method not implemented"

  def handle_bin(self, line):
     raise NotImplemented, "method not implemented"

  def handle_scalar(self, line):
     raise NotImplemented, "method not implemented"

  def handle_scalar(self, attr):
     raise NotImplemented, "method not implemented"

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
