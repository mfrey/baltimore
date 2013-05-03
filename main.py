#!/usr/bin/env python2.7

import argparse

from representation import scalarfile as scalar
from analysis import packetdeliveryrateanalysis as pdr
from configuration import configuration as cfg

def main():
  parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
  parser.add_argument('-d', dest='directory', type=str, default=".", action='store', help='a directory which contains OMNeT++ result files')
  parser.add_argument('-v', dest='verbose', default=False, const=True, action='store_const', help="print out verbose information for each iteration")

  arguments = parser.parse_args()
  configuration = cfg.Configuration()
  configuration.read_directory(arguments.directory)
  
  currentExperimentNr = 1
  for experimentName in configuration.experiments:
    nrOfIterations = len(configuration.experiments[experimentName])
    print
    print 'Processing experiment %d "%s"' % (currentExperimentNr, experimentName)
    print '=' * 55
    
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
      sumOfLoops += analyser.routing_loop_detected
      sumOfRouteFailures += analyser.route_failures
      sumOfFailedDiscoveries += analyser.route_discovery_failed
      sumOfTTLDrops += analyser.time_to_live_expired
      sumOfInexplicableLosses += analyser.inexplicable_loss
      
      if arguments.verbose:
        print replication.run
        print analyser
    
    avgNrOfSentPackets = sumOfSentPackets/float(nrOfIterations)
    print "Overall statistics (averaged over %d iterations)" % nrOfIterations
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

