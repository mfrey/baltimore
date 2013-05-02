#!/usr/bin/env python2.7

import os

class Configuration:
  def __init__(self):
    self.scalar_files = []

  def read_directory(self, directory): 
    files = [(x[0], x[2]) for x in os.walk(directory)] 
    for d in files:
      # the first entry holds the directory
      current_directory = d[0]
      # the second entry holds the content of the directory
      current_directory_files = d[1]

      for f in current_directory_files: 
        if f.endswith("sca"):
          self.scalar_files.append(current_directory + "/" + f) 

