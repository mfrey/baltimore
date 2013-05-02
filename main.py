#!/usr/bin/env python2.7

from representation import scalarfile as scalar
from analysis import packetdeliveryrateanalysis as pdr

def main():
  scalarParser = scalar.ScalarFile()
  scalarParser.read("scenario.sca")
#  parser = argparse.ArgumentParser(description='evaluation script for the ara-sim framework')
#  arguments = parser.parse_args()
  pdrAnalysis = pdr.PacketDeliveryRateAnalysis()
  pdrAnalysis.evaluate(scalarParser.nodes)
  print pdrAnalysis

if __name__ == "__main__":
  main()
