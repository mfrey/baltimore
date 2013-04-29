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
      
      # preparte the reg exp to match node[number]
      pattern = re.compile('node\[\d\]')
      node_identifier = -1
      
      node = n.Node()
      node.identifier = node_identifier

      for line in f:
        result = pattern.findall(line)            

        if len(result) != 0:
          # get the node from the string
          identifier = result[0].split('[')[1].split(']')[0]

          if node.identifier != -1:
            if identifier != node.identifier:        
              # push the current node
              result_arr.append(node) 
              # create a new node
              node = n.Node()
              node.identifier = identifier
          else:
            node.identifier = identifier

#          print result
        
      print len(result_arr)
      

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
