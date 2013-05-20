#!/usr/bin/env python2.7

import ConfigParser

class Configuration(object):
  def __init__(self, file_name):
	self.config = ConfigParser.ConfigParser()
	self.config.read(file_name)
	# absolut path to the ara-sim simulation binary
	self.configuarion["simulation_binary"] = self.config.get('General', 'binary')
	# absolut path to the omnetpp.ini
	self.configuration["omnetpp_ini"] = self.config.get('General', 'omnetpp_ini')
	# a list of ned files which shall be considered for the simulation
	self.configuration["ned_files"] = self.config.get('General', 'ned_files')
	# the total number of repetitions to execute
	self.configuration["repetitions"] = self.config.get('General', 'repetitions')
	# the total number of repetitions to execute
	self.configuration["scenarios"] = self.config.get('General', 'scenarios')



