#!/usr/bin/env python2.7

import re

from plot import packetdeliveryrateplot as pdrplot
from analysis import packetdeliveryrateanalysis as pdr

class Experiment:
  def __init__(self):
    self.name = ""
    self.description = ""
    self.scalar_files = [] 
    self.vector_files = [] 
    self.packet_delivery_rate_analysis = {}

  def evaluate(self):
    # first we aggregate
    for repetition in self.scalar_files:
      self.aggregate_packet_delivery_rate(repetition)

    # than we analyze/evaluate
    self.analyze_packet_delivery_rate()

  def evaluate_packet_delivery_rate(self, repetition):
    self.aggregate_packet_delivery_rate(repetition)
    self.analyze_packet_delivery_rate(repetition)

  """ the method aggregates the packet delivery rate over all repetitions """
  def aggregate_packet_delivery_rate(self, repetition):
	 # analyze the current repetition
	 packetDeliveryRateAnalysis = pdr.PacketDeliveryRateAnalysis()
	 packetDeliveryRateAnalysis.evaluate(repetition.nodes)
	 # store the result of the analysis as a list
	 self.packet_delivery_rate_analysis[repetition] = packetDeliveryRateAnalysis.to_list()

  """ the method analyzes the packet delivery rate over all repetitions """
  def analyze_packet_delivery_rate(self):
    if len(self.packet_delivery_rate_analysis) > 1:
      sum_pdr = [sum(entries) for entries in zip(*self.packet_delivery_rate_analysis.values())]
    else:
      sum_pdr = self.packet_delivery_rate_analysis.values()[0]

    avg_pdr = [entry/float(len(self.packet_delivery_rate_analysis)) for entry in sum_pdr]


    # TODO: make a seperate method for that
    print
    print 'Processing experiment ', self.name
    print '=' * 55
    print "Overall statistics (averaged over %d iterations)" % len(self.packet_delivery_rate_analysis)
    self.print_statistics("Sent Packets", avg_pdr[0], avg_pdr[0])
    self.print_statistics("Received Packets", avg_pdr[0], avg_pdr[1])
    self.print_statistics("Routing Loops", avg_pdr[0], avg_pdr[3])
    self.print_statistics("Route Failures", avg_pdr[0], avg_pdr[2])
    self.print_statistics("Failed Route Discoveries", avg_pdr[0], avg_pdr[4])
    self.print_statistics("Dropped Packets (TTL = 0)", avg_pdr[0], avg_pdr[5])
    self.print_statistics("Inexplicable loss", avg_pdr[0], avg_pdr[6])
    print "\n"
    
  def print_statistics(self, name, avgNrOfSentPackets, value):
    if avgNrOfSentPackets > 0:
      percent = "%6.2f%%" % ((value/float(avgNrOfSentPackets)) * 100.0)
    else:
      percent = "  0.00%%"
 
    maxNumberOfDigits = len(str(avgNrOfSentPackets))
    print "%-26s %*d\t" % (name, maxNumberOfDigits, value) + percent

  # TODO: fixme	   
  def draw_packet_delivery_rate(self):
    xlist = []
    ylist = []
    
    for key in self.packet_delivery_rate_analysis:
      # TODO: make a better reg exp
      numbers = re.findall(r'\d+', key.fileName)
      xlist.append(numbers[len(numbers)-1])
      ylist.append(self.packet_delivery_rate_analysis[key][1]/float(self.packet_delivery_rate_analysis[key][0]))

    plot = pdrplot.PacketDeliveryRatePlot()
    plot.xlist = xlist
    plot.ylist = ylist
    plot.draw("todo_" + self.name + ".png")

