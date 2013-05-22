#!/usr/bin/env python2.7

import ConfigParser

class Configuration(object):
  def __init__(self, file_name):
	self.config = ConfigParser.ConfigParser()
	self.config.read(file_name)
	# absolut path to the ara-sim simulation binary
	self.settings["simulation_binary"] = self.config.get('General', 'binary')
	# absolut path to the omnetpp.ini
	self.settings["omnetpp_ini"] = self.config.get('General', 'omnetpp_ini')
	# a list of ned files which shall be considered for the simulation
	self.settings["ned_files"] = self.config.get('General', 'ned_files')
	# the total number of repetitions to execute
	self.settings["repetitions"] = self.config.get('General', 'repetitions')
	# the name of the scenarios to run (currently only supporting one) 
	self.settings["scenarios"] = self.config.get('General', 'scenarios')
        # the ld_library_path
        self.settings["ld_library_path"] = self.config.get('General', 'ld_library_path')
        # the cwd (where the ned files of the simulation reside
	self.settings["cwd"]  = self.config.get('General', 'cwd')
