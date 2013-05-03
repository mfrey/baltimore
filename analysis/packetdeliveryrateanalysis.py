#!/usr/bin/env python2.7

class PacketDeliveryRateAnalysis:

  def __init__(self):
    self.clear()

  def clear(self):
    self.sent = 0
    self.received = 0
    self.routeFailures = 0
    self.routingLoopDetected = 0
    self.routeDiscoveryFailed = 0
    self.timeToLiveExpired = 0
    self.inexplicableLoss = 0

  def evaluate(self, nodes):
    for node in nodes:
      self.sent += int(self.get_metric(nodes, node, "trafficSent"))
      self.received += int(self.get_metric(nodes, node, "trafficReceived"))
      self.routeFailures += int(self.get_metric(nodes, node, "routeFailure:count"))
      self.routingLoopDetected += int(self.get_metric(nodes, node, "routingLoopDetected:count"))
      self.routeDiscoveryFailed += int(self.get_metric(nodes, node, "packetUnDeliverable:count"))
      self.timeToLiveExpired += int(self.get_metric(nodes, node, "dropZeroTTLPacket:count"))
    
    self.inexplicableLoss = self.sent - self.received - self.routingLoopDetected - self.routeFailures - self.routeDiscoveryFailed - self.timeToLiveExpired

    if self.inexplicableLoss < 0:
      self.inexpclicableLoss = 0
      
    self.pdr = float(self.received)/float(self.sent)

  def get_metric(self, database, identifier, metric):
    result = -1
    try: 
      result = database[identifier].results[metric]
      return result;
    except KeyError:
      print "unknown key ", metric, " for node ", identifier 
      
  def __str__(self):
    result  = self.get_result_line("Sent Packets", self.sent)
    result += self.get_result_line("Received Packets", self.received)
    result += self.get_result_line("Route Failures", self.routeFailures)
    result += self.get_result_line("Failed Route Discoveries", self.routeDiscoveryFailed)
    result += self.get_result_line("Dropped Packets (TTL = 0)", self.timeToLiveExpired) 
    result += self.get_result_line("Inexplicable loss", self.inexplicableLoss)
    result += '=' * 39 + "\n"
    return result

  def get_result_line(self, name, value):
    if self.sent > 0:
      percent = "%6.2f%%" % ((float(value)/float(self.sent)) * 100.0)
    else:
      percent = "  0.00%%"
    
    name += ":"
    maxNumberOfDigits = len(str(self.sent))
    return "%-26s %*d\t" % (name, maxNumberOfDigits, value) + percent + "\n" 
