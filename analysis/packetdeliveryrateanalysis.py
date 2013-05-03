#!/usr/bin/env python2.7

class PacketDeliveryRateAnalysis:

  def __init__(self):
    self.sent = 0
    self.received = 0
    self.routeFailures = 0
    self.routingLoopDetected = 0
    self.routeDiscoveryFailed = 0
    self.timeToLiveExpired = 0
    self.inexplicableLoss = 0

  def evaluate(self, nodes):
    for node in nodes:
      self.sent = self.sent + int(self.get_metric(nodes, node, "trafficSent"))
      self.received = self.received + int(self.get_metric(nodes, node, "trafficReceived"))
      self.routeFailures = self.routeFailures + int(self.get_metric(nodes, node, "routeFailure:count"))
      self.routingLoopDetected = self.routingLoopDetected + int(self.get_metric(nodes, node, "routingLoopDetected:count"))
      self.routeDiscoveryFailed = self.routeDiscoveryFailed + int(self.get_metric(nodes, node, "packetUnDeliverable:count"))
      self.timeToLiveExpired = self.timeToLiveExpired + int(self.get_metric(nodes, node, "dropZeroTTLPacket:count"))
    self.inexplicableLoss = self.sent - self.received - self.routingLoopDetected - self.routeFailures - self.routeDiscoveryFailed - self.timeToLiveExpired

    if self.inexplicableLoss < 0:
      self.inexpclicableLoss = 0

  def get_metric(self, database, identifier, metric):
    result = -1
    try: 
      result = database[identifier].results[metric]
      return result;
    except KeyError:
      print "unknown key ", metric, " for node ", identifier 
      
  def __str__(self):
    result = "Sent Packets:              " + str(self.sent) + "\n"
    result = result + "Received Packets:          " + str(self.received) + ", " + self.get_percentage(self.received)
    result = result + "Route Failures:            " + str(self.routeFailures) + ", " + self.get_percentage(self.routeFailures)
    result = result + "Failed Route Discoveries:  " + str(self.routeDiscoveryFailed) + ", " + self.get_percentage(self.routeDiscoveryFailed)
    result = result + "Dropped Packets (TTL = 0): " + str(self.timeToLiveExpired) + ", " + self.get_percentage(self.timeToLiveExpired) 
    result = result + "Inexplicable loss:         " + str(self.inexplicableLoss) + ", " + self.get_percentage(self.inexplicableLoss) 
    return result

  def get_percentage(self, value):
    if self.sent > 0:
      result = (float(value)/float(self.sent))*100.0
      return str("{0:.2f}".format(round(result, 2))) + " % \n" 
    return "\n"

  def get_packet_delivery_rate(self):
    if self.sent > 0:
      result = (float(self.received)/float(self.sent))*100.0
      return "{0:.2f}".format(round(result, 2)) 
    return 0.0

  def clear(self):
    self.sent = 0
    self.received = 0
    self.routeFailures = 0
    self.routingLoopDetected = 0
    self.routeDiscoveryFailed = 0
    self.timeToLiveExpired = 0
    self.inexplicableLoss = 0