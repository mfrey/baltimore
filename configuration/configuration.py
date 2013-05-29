#!/usr/bin/env python2.7

import multiprocessing

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
                'repetitions': int(parser.get('General', 'repetitions')),
                'cpu_cores' : self._get_nr_of_cpus(parser.get('General', 'cpu_cores'))
            }

            try:
                self.settings['db_host'] = parser.get('Database', 'host_name')
				self.settings['db_port'] = int(parser.get('Database', 'port'))
                self.settings['db_db'] = parser.get('Database', 'database')
                self.settings['db_user'] = parser.get('Database', 'user')
                self.settings['db_password'] = parser.get('Database', 'password')
                self.settings['db_settings'] = True
            except NoSectionError:
                self.settings['db_settings'] = False
        
            self._build_ned_path()
            self._build_omnetpp_ini_path()
            self._build_ld_library_path()
            self._build_cwd()
            self._build_scenarios(parser.get('General', 'scenarios'))
        else:
            self.settings = {}

    def _get_absolute_path(self, some_path):
        return path.abspath(path.expanduser(some_path))

    def _get_nr_of_cpus(self, wanted_cores):
        nr_of_existing_cpu_cores = multiprocessing.cpu_count()
        
        if wanted_cores == '*':
            return nr_of_existing_cpu_cores
        else:
            wanted_cores = int(wanted_cores)
            if nr_of_existing_cpu_cores == 1:
               return 1
            elif nr_of_existing_cpu_cores < wanted_cores:
               return int(nr_of_existing_cpu_cores / 2)
            else:
               return wanted_cores
    
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
        config.settings['cpu_cores'] = self._get_nr_of_cpus('*')
        return config
