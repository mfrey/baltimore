#!/usr/bin/env python2.7

from plot import packetdeliveryrateplot as pdrplot
from analysis import packetdeliveryrateanalysis as pdr

class Experiment:
  def __init__(self):
    self.experiment_identifer = ""
    self.experiment_description = ""
    self.scalar_files = [] 
    self.vector_files = [] 
    self.packet_delivery_rates = {}

  def analyze_packet_delivery_rate(self):
    pdrAnalysis = pdr.PacketDeliveryRateAnalysis()
    for scalar_file in self.scalar_files:
      scalarParser.read(scalar_file)
      pdrAnalysis.evaluate(scalarParser.nodes)
      # TODO: key should be probably a better value
      self.packet_delivery_rates[scalar_file] = pdrAnalysis.get_packet_delivery_rate()
      pdrAnalysis.clear()
    
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
