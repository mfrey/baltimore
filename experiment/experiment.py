#!/usr/bin/env python2.7

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
	for repetition in self.scalar_files:
	  self.evaluate_packet_delivery_rate(repetition)

  """ the method aggregates the packet delivery rate over all repetitions """
  def aggregate_packet_delivery_rate(self, repetition):
	 # analyze the current repetition
	 packetDeliveryRateAnalysis = pdr.PacketDeliveryRateAnalysis()
	 packetDeliveryRateAnalysis.evaluate(repetition.nodes)
	 # store the result of the analysis as a list
	 self.packet_delivery_rate_analysis[repetition] = packetDeliveryRateAnalysis.to_list()

  """ the method analyzes the packet delivery rate over all repetitions """
  def analyze_packet_delivery_rate():
	if len(self.packet_delivery_rate_analysis) > 1:
	  sum_pdr = [sum(entries) for entries in zip(*self.packet_delivery_rate_analysis.values())]
	else:
	  sum_pdr = self.packet_delivery_rate_analysis.values()[0]
	return sum_pdr
	   
  def draw_packet_delivery_rate(self):
    xlist = []
    ylist = []
    for key, value in self.packet_delivery_rates:
      xlist.append(key)
      ylist.append(value)

    plot = pdrplot.PacketDeliveryRatePlot()
    plot.xlist = xlist
    plot.ylist = ylist
    plot.draw("todo.png")

