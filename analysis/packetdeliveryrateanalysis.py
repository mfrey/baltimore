#!/usr/bin/env python2.7

class PacketDeliveryRateAnalysis:
  # TODO: build up a string instead of a simple print
  def __str__(self):
	print "Sent Packets:     ", self.sent

	if self.sent > 0:
	  print "Received Packets: ", self.received, " ", (self.received/self.sent * 100), "%" 
	else:
	  print "Received Packets: ", self.received 

	print "Route Failures:   ", self.routeFailures


  def __init__(self):
	self.sent = 0
	self.received = 0
	self.loops = 0
	self.routeFailures = 0

  def evaluate(self, nodes):
	for node in nodes:
	  try:
		self.sent = self.sent + int(nodes[node].results["trafficSent"])
		self.received = self.received + int(nodes[node].results["trafficReceived"])
		self.routeFailures = self.routeFailures + int(nodes[node].results["routeFailure:count"])

	  except KeyError:
		print "unknown key "





