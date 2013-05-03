#!/usr/bin/env python2.7

class PacketDeliveryRateAnalysis:

  def __init__(self):
    self.clear()

  def clear(self):
    self.sent = 0
    self.received = 0
    self.route_failures = 0
    self.routing_loop_detected = 0
    self.route_discovery_failed = 0
    self.time_to_live_expired = 0
    self.inexplicable_loss = 0

  def evaluate(self, nodes):
    for node in nodes:
      self.sent += int(self.get_metric(nodes, node, "trafficSent"))
      self.received += int(self.get_metric(nodes, node, "trafficReceived"))
      self.route_failures += int(self.get_metric(nodes, node, "routeFailure:count"))
      self.routing_loop_detected += int(self.get_metric(nodes, node, "routingLoopDetected:count"))
      self.route_discovery_failed += int(self.get_metric(nodes, node, "packetUnDeliverable:count"))
      self.time_to_live_expired += int(self.get_metric(nodes, node, "dropZeroTTLPacket:count"))
    
    self.inexplicable_loss = self.sent - self.received - self.routing_loop_detected - self.route_failures - self.route_discovery_failed - self.time_to_live_expired

    if self.inexplicable_loss < 0:
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
    result += self.get_result_line("Routing Loops", self.routing_loop_detected)
    result += self.get_result_line("Route Failures", self.route_failures)
    result += self.get_result_line("Failed Route Discoveries", self.route_discovery_failed)
    result += self.get_result_line("Dropped Packets (TTL = 0)", self.time_to_live_expired) 
    result += self.get_result_line("Inexplicable loss", self.inexplicable_loss)
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

  """ the method returns a list of the attributes of the packet delivery rate analysis"""
  def to_list(self):
	return [self.sent, self.received, self.route_failures, self.routing_loop_detected, self.route_discovery_failed, self.time_to_live_expired, self.inexplicable_loss]
