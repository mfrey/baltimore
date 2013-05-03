#!/usr/bin/env python2.7

import argparse

from representation import scalarfile as scalar
from analysis import packetdeliveryrateanalysis as pdr
from configuration import configuration as cfg

def main():
  parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
  parser.add_argument('-d', dest='directory', type=str, default=".", action='store', help='a directory which contains OMNeT++ result files')

  arguments = parser.parse_args()
  directory = arguments.directory
  configuration = cfg.Configuration()
  configuration.read_directory(directory)
  
  currentExperimentNr = 1
  for experimentName in configuration.experiments:
    nrOfIterations = len(configuration.experiments[experimentName])
    print
    print 'Processing experiment %d "%s" with %d iterations' % (currentExperimentNr, experimentName, nrOfIterations)
    print '=' * 54
    
    pdrSum = 0
    sumOfSentPackets = 0
    sumOfReceivedPackets = 0
    sumOfLoops = 0
    sumOfRouteFailures = 0
    sumOfFailedDiscoveries = 0
    sumOfTTLDrops = 0
    sumOfInexplicableLosses = 0
    for replication in configuration.experiments[experimentName]:
      analyser = pdr.PacketDeliveryRateAnalysis()      
      analyser.evaluate(replication.nodes)
      pdrSum += analyser.pdr
      sumOfSentPackets +=analyser.sent
      sumOfReceivedPackets += analyser.received
      sumOfLoops += analyser.routingLoopDetected
      sumOfRouteFailures += analyser.routeFailures
      sumOfFailedDiscoveries += analyser.routeDiscoveryFailed
      sumOfTTLDrops += analyser.timeToLiveExpired
      sumOfInexplicableLosses += analyser.inexplicableLoss
    
    avgNrOfSentPackets = sumOfSentPackets/float(nrOfIterations)
    print_statistics("Sent Packets", avgNrOfSentPackets, avgNrOfSentPackets)
    print_statistics("Received Packets", avgNrOfSentPackets, sumOfReceivedPackets/float(nrOfIterations))
    print_statistics("Routing Loops", avgNrOfSentPackets, sumOfLoops/float(nrOfIterations))
    print_statistics("Route Failures", avgNrOfSentPackets, sumOfRouteFailures/float(nrOfIterations))
    print_statistics("Failed Route Discoveries", avgNrOfSentPackets, sumOfFailedDiscoveries/float(nrOfIterations))
    print_statistics("Dropped Packets (TTL = 0)", avgNrOfSentPackets, sumOfTTLDrops/float(nrOfIterations))
    print_statistics("Inexplicable loss", avgNrOfSentPackets, sumOfInexplicableLosses/float(nrOfIterations))
    print "\n"
    currentExperimentNr += 1   

def print_statistics(name, avgNrOfSentPackets, value):
  if avgNrOfSentPackets > 0:
    percent = "%6.2f%%" % ((value/float(avgNrOfSentPackets)) * 100.0)
  else:
    percent = "  0.00%%"
 
  maxNumberOfDigits = len(str(avgNrOfSentPackets))
  print "%-26s %*d\t" % (name, maxNumberOfDigits, value) + percent

if __name__ == "__main__":
  main()
