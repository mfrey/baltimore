#!/usr/bin/env python2.7

import multiprocessing

from os import path
from ConfigParser import ConfigParser, NoSectionError

class Configuration(object):
    def __init__(self, file_name):
        if(file_name is not None):
            self.parser = ConfigParser()
            self.parser.read(file_name)

            self.settings = {
                'ara_home': self._get_absolute_path(self._get('General', 'ara_home')),
                'omnetpp_home': self._get_absolute_path(self._get('General', 'omnetpp_home')),
                'scenario_home': self._get('General', 'scenario_home'),
                'repetitions': int(self._get('General', 'repetitions')),
                'cpu_cores' : self._get_nr_of_cpus(self._get('General', 'cpu_cores'))
            }

            self.set_database_options()
            self.set_analysis_options()
            self.set_testbed_options()

            self._build_ned_path()
            self._build_omnetpp_ini_path()
            self._build_ld_library_path()
            self._build_cwd()
            self._build_scenarios(self._get('General', 'scenarios'))

        else:
            self.settings = {}


    def set_database_options(self):
        self.settings['db_settings'] = True
        self.settings['db_host'] = self._get('Database', 'host_name')
        self.settings['db_port'] = int(self._get('Database', 'port'))
        self.settings['db_db'] = self._get('Database', 'database')
        self.settings['db_user'] = self._get('Database', 'user')
        self.settings['db_password'] = self._get('Database', 'password')


    def set_analysis_options(self):
        self.settings['analysis_settings'] = True
        self.settings['analysis_routing_table_trace'] = self._get_boolean_option('Analysis', 'routing_table_trace')
        self.settings['analysis_location'] = path.expanduser(self._get('Analysis', 'location'))
        self.settings['analysis_generation'] = self._get_boolean_option('Analysis', 'generate_plots_during_runtime')
        self.settings['analysis_csv'] = self._get_boolean_option('Analysis', 'export_csv_data')
        self.settings['analysis_network'] = self._get_boolean_option('Analysis', 'network')


    def set_testbed_options(self):
        self.settings['testbed_settings'] = True
        self.settings['testbed_interface'] = self._get('Testbed', 'interface')


    def _get(self, section, option):
        try:
           result = self.parser.get(section, option)
        except NoOptionError:
           self.logger.debug("no such option %s in section %s", option, section)
           result = ""
        except NoSectionError: 
           result = ""
           self.settings[section + "_settings"] = False
           self.logger.debug("no such section %s", section)

        return result


    def _get_boolean_option(self, section, option):
        try:
           result = self.parser.getboolean(section, option)
        except NoOptionError:
           self.logger.debug("no such option %s in section %s", option, section)
           result = False
        except NoSectionError: 
           result = False
           self.settings[section + "_settings"] = False
           self.logger.debug("no such section %s", section)

        return result


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
