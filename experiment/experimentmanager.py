#!/usr/bin/env python2.7

import os
import sys
import logging

# TODO: check that
import experiment as exp

from representation import scalarfile as scalar

class ExperimentManager:
  def __init__(self):
    self.scalar_files = []
    self.vector_files = []
    self.experiments = {}

  """ The method reads a directory and parses scalar files made by OMNeT++ """
  def read_directory(self, directory, scenario): 
    # TODO: change this to logging, so we only print it if required
    print 'Scanning directory "%s" for simulation result files.\nThis may take some time depending on the number of files...' % directory

    files = [(x[0], x[2]) for x in os.walk(directory)]
    for d in files:
      # the first entry holds the directory
      current_directory = d[0]
      # the second entry holds the content of the directory
      current_directory_files = d[1]

      for file in current_directory_files: 
        if file.endswith("sca"):
          sys.stdout.write(".")
          sys.stdout.flush()
          file_name = current_directory + "/" + file
          if scenario == "":
            self.read_file(file_name)
          else:
            if file.startswith(scenario):
              self.read_file(file_name)
           
    number_read_scalar_files = sum([len(scalar_files) for scalar_files in self.experiments.values()])
    # TODO: change this to logging, so we only print it if required
    print "\n\nSuccessfully read %d experiment(s) from %d scalar file(s)." % (len(self.experiments), number_read_scalar_files)
    
  """ The method reads a scalar file made by OMNeT++ """
  def read_file(self, file_name):
     if file_name.endswith("sca"):
       sys.stdout.write(".")
       sys.stdout.flush()
       result_file = scalar.ScalarFile(file_name)
       result_file.read_file()
          
       if result_file.experiment not in self.experiments:
         self.experiments[result_file.experiment] = []
          
       self.experiments[result_file.experiment].append(result_file)

  def evaluate(self, verbose):
    for experiment in self.experiments:
      self.evaluate_experiment(experiment, verbose)  

  def evaluate_experiment(self, experiment_identifier, verbose):
    # TODO: we should directly create a experiment object while reading the scalar files. This is a temporary fix
    experiment = exp.Experiment()
    experiment.name = experiment_identifier
    experiment.scalar_files = self.experiments[experiment_identifier]

    experiment.evaluate(verbose)
