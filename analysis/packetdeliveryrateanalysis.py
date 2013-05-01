#!/usr/bin/env python2.7

class PacketDeliveryRateAnalysis:
  def evaluate(self, nodes):
	sent = 0
	received = 0

	for node in nodes:
	  #sent = sent + nodes[node]["trafficSent"]
	  print nodes[node].results["trafficSent"]
	  #received = received + nodes[node]["trafficReceived"]

	print "packet delivery rate is ", (received/sent * 100)


