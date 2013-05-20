#!/usr/bin/env python2.7

import os

from subprocess import call

class Runner(object):
  def __init__(self, scenario, repetition, ned_path, omnetpp_ini, binary, ld_library_path):
	self.scenario = scenario
	self.repetition = repetition
	self.ned_path = ned_path
	self.omnetpp_ini = omnetpp_ini
	self.binary = binary
	self.ld_library_path = ld_library_path

  @classmethod
  def run_simulation(cls, args):
	self = cls(*args)
	self.run()

  def run(self):
	environment = dict(os.environ)
	environment["LD_LIBRARY_PATH"] = self.ld_library_path

	call([self.binary, "-r", self.repetition, "-u", "Cmdenv", "-c", self.scenario, "-n", self.ned_path, self.omnetpp_ini], env=environment)

if __name__ == "__main__":
  binary = "/home/michael/Desktop/Projekte/code/ara-sim/omnetpp/ara-sim"
  repetition = "1"
  scenario = "midSize"
  omnetpp_ini = "/home/michael/Desktop/Projekte/code/ara-sim/simulations/static/omnetpp.ini"
  ned_path = "/home/michael/Desktop/Projekte/code/ara-sim/inetmanet/src:/home/michael/Desktop/Projekte/code/ara-sim/inetmanet/examples:/home/michael/Desktop/Projekte/code/ara-sim/:/home/michael/Desktop/Projekte/code/ara-sim/omnetpp"
  ld_library_path = "$LD_LIBRARY_PATH:/home/michael/Desktop/Projekte/code/ara-sim/src:/home/michael/Desktop/Projekte/code/ara-sim/inetmanet/src"

  runner = Runner(scenario, repetition, ned_path, omnetpp_ini, binary, ld_library_path)
  runner.run()

