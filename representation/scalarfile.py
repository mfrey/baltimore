#!/usr/bin/env python2.7

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
    with open(filename, "r") as f:
      # handle the preamble of the scalar file
      preamble = f.readlines()[:16]
      self.handle_preamble(preamble)

      #for _ in xrange(18):
      #  next(f)

      for line in f:
        print f

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
