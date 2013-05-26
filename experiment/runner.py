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

