#!/usr/bin/env python2.7

import ConfigParser

class Configuration(object):
    def __init__(self, file_name):
        self.config = ConfigParser.ConfigParser()
	self.config.read(file_name)

        self.settings = {}

        self.settings["ara_home"] = self.config.get('General', 'ara_home')
        self.settings['scenario_home'] = self.config.get('General', 'scenario_home')
	self.settings["repetitions"] = int(self.config.get('General', 'repetitions'))

	self._build_ned_path()
	self._build_omnetpp_ini_path()
        self._build_ld_library_path()
	self._build_cwd()
	self._build_scenarios()

    def _build_ned_path(self):
        self.settings['ned_path'] =  self.settings['ara_home'] + '/inetmanet/src:' + self.settings['ara_home'] + '/inetmanet/examples:' + self.settings['ara_home'] + '/omnetpp:' + self.settings['ara_home'] + '/simulations/' + self.settings['scenario_home']

    def _build_omnetpp_ini_path(self):
        self.settings['omnetpp_ini'] = self.settings['ara_home'] + '/simulations/' + self.settings['scenario_home'] + '/omnetpp.ini'

    def _build_ld_library_path(self):
        self.settings['ld_library_path'] = "$LD_LIBRARY_PATH:" + self.settings['ara_home'] + '/src:' + self.settings['ara_home'] + '/inetmanet/src'

    def _build_cwd(self):
        self.settings['cwd'] = self.settings['ara_home'] + '/simulations/' + self.settings['scenario_home'] 

    def _build_scenarios(self):
        self.settings['scenarios'] = [scenario.strip() for scenario in self.config.get('General', 'scenarios').split(',')]
