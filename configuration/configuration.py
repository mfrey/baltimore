#!/usr/bin/env python2.7

import os
import sys

from representation import scalarfile as scalar

class Configuration:
  def __init__(self):
    self.scalar_files = []
    self.experiments = {}

  def read_directory(self, directory): 
    print 'Scanning directory "%s" for simulation result files.\nThis may take some time depending on the number of files...' % directory
    nrOfReadScalarFiles = 0

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
          resultFile = scalar.ScalarFile(current_directory + "/" + file)
          resultFile.read_file()
          nrOfReadScalarFiles += 1
          #self.scalar_files.append(current_directory + "/" + f)
          
          if resultFile.experiment not in self.experiments:
            self.experiments[resultFile.experiment] = []
          
          self.experiments[resultFile.experiment].append(resultFile)
           
    print "\n\nSuccessfully read %d experiment(s) from %d scalar file(s)." % (len(self.experiments), nrOfReadScalarFiles)
    
