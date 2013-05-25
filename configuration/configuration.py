#!/usr/bin/env python2.7

from os import path 
from ConfigParser import ConfigParser

class Configuration(object):
    
    def __init__(self, file_name):
        if(file_name is not None):
            parser = ConfigParser()
            parser.read(file_name)
            
            self.settings = {
                'ara_home': self._get_absolute_path(parser.get('General', 'ara_home')),
                'omnetpp_home': self._get_absolute_path(parser.get('General', 'omnetpp_home')),
                'scenario_home': parser.get('General', 'scenario_home'),
                'repetitions': int(parser.get('General', 'repetitions'))
            }
        
            self._build_ned_path()
            self._build_omnetpp_ini_path()
            self._build_ld_library_path()
            self._build_cwd()
            self._build_scenarios(parser.get('General', 'scenarios'))
        else:
            self.settings = {}
    
    def _get_absolute_path(self, some_path):
        return path.abspath(path.expanduser(some_path))
    
    def _build_ned_path(self):
        self.settings['ned_path'] =  self.settings['ara_home'] + '/inetmanet/src:' + self.settings['ara_home'] + '/inetmanet/examples:' + self.settings['ara_home'] + '/omnetpp:' + self.settings['ara_home'] + '/simulations/' + self.settings['scenario_home']
    
    def _build_omnetpp_ini_path(self):
        self.settings['omnetpp_ini'] = self.settings['ara_home'] + '/simulations/' + self.settings['scenario_home'] + '/omnetpp.ini'
    
    def _build_ld_library_path(self):
        self.settings['ld_library_path'] = "$LD_LIBRARY_PATH:" + self.settings['ara_home'] + '/src:' + self.settings['ara_home'] + '/inetmanet/src:' + self.settings['omnetpp_home'] + '/lib'  
    
    def _build_cwd(self):
        self.settings['cwd'] = self.settings['ara_home'] + '/simulations/' + self.settings['scenario_home'] 
    
    def _build_scenarios(self, scenarios):
        self.settings['scenarios'] = [scenario.strip() for scenario in scenarios.split(',')]

    @staticmethod
    def createDefaultConfiguration():
        config = Configuration(None);
        config.settings['cwd'] = "."
        config.settings['repetitions'] = 1
        config.settings['ld_library_path'] = "$LD_LIBRARY_PATH"
        config.settings['scenarios'] = ['']
        return config
