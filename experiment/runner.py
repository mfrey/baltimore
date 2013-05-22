#!/usr/bin/env python2.7

import os

from subprocess import call

def run_simulation(args):
  return Runner(*args).run()

class Runner(object):
  def __init__(self, scenario, repetition, settings):
	self.scenario = scenario
	self.repetition = repetition
	# todo
	self.ned_path = settings['ned_files']
	self.omnetpp_ini = settings['omnetpp_ini']
	self.binary = settings['binary']
	self.ld_library_path = settings['ld_library_path']
	self.cwd = settings['cwd']


  def run(self):
	environment = dict(os.environ)
	environment["LD_LIBRARY_PATH"] = self.ld_library_path
	call([self.binary, "-r", str(self.repetition), "-u", "Cmdenv", "-c", self.scenario, "-n", self.ned_path, self.omnetpp_ini], env=environment, cwd=self.cwd)

# this is just for testing purposes and will be removed soon
#if __name__ == "__main__":
#  binary = "/home/michael/Desktop/Projekte/code/ara-sim/omnetpp/ara-sim"
#  repetition = "1"
#  scenario = "midSize"
#  omnetpp_ini = "/home/michael/Desktop/Projekte/code/ara-sim/simulations/static/omnetpp.ini"
#  ned_path = "/home/michael/Desktop/Projekte/code/ara-sim/inetmanet/src:/home/michael/Desktop/Projekte/code/ara-sim/inetmanet/examples:/home/michael/Desktop/Projekte/code/ara-sim/simulations/static:/home/michael/Desktop/Projekte/code/ara-sim/omnetpp"
#  ld_library_path = "$LD_LIBRARY_PATH:/home/michael/Desktop/Projekte/code/ara-sim/src:/home/michael/Desktop/Projekte/code/ara-sim/inetmanet/src"
#  cwd = "/home/michael/Desktop/Projekte/code/ara-sim/simulations/static"
#  runner = Runner(scenario, repetition, ned_path, omnetpp_ini, binary, ld_library_path, cwd)
#  runner.run()

