#!/usr/bin/env python2.7

import argparse

from representation import scalarfile as scalar
from analysis import packetdeliveryrateanalysis as pdr
from configuration import configuration as cfg

def main():
  scalarParser = scalar.ScalarFile()
  parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
  parser.add_argument('-d', dest='directory', type=str, default=".", action='store', help='a directory which contains OMNeT++ result files')

  arguments = parser.parse_args()
  directory = arguments.directory
  configuration = cfg.Configuration()
  configuration.read_directory(directory)

  for scalar_file in configuration.scalar_files:
    print scalar_file
    scalarParser.read(scalar_file)
    pdrAnalysis = pdr.PacketDeliveryRateAnalysis()
    pdrAnalysis.evaluate(scalarParser.nodes)
    print pdrAnalysis
    pdrAnalysis.clear()
    print ""

if __name__ == "__main__":
  main()
