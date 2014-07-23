#!/usr/bin/env python3

import hashlib
import os
from configparser import ConfigParser


class OMNeTConfigurationFileParser:
    def __init__(self, file_name):
        self.omnetpp_ini_file = ConfigParser(allow_no_value=True)
        self.omnetpp_ini_hash = hashlib.sha512(file_name.encode(encoding='UTF-8',errors='strict')).hexdigest()
        self.standard_ini_hash = "0"
        self.omnetpp_ini_file.read(file_name)
        self.file_name = file_name

        self._handle_include_if_existent()

    def _handle_include_if_existent(self):
        if self._has_include('General'):
            include_file = self._get_include_file_name()
            if os.path.isfile(include_file):
                settings = self._parse_include_file(include_file)
                self._merge_settings(settings)

    def _get_include_file_name(self):
        additional_config_file_name = ""

        for key, value in self.get_section('General'):
            if key.startswith('include'):
                additional_config_file_name = value
                break

        additional_config_file_path = self.file_name.replace('omnetpp.ini', additional_config_file_name)
        return additional_config_file_path

    def _parse_include_file(self, file_name):
        parser = ConfigParser()
        self.standard_ini_hash = hashlib.sha512(file_name.encode(encoding='UTF-8',errors='strict')).hexdigest()
        parser.read(file_name)
        return parser

    def _merge_settings(self, settings):
        for key, value in settings.items('General'):
            if key not in self.get_section('General'):
                self.omnetpp_ini_file.set('General', key, value)

    def _get_keys(self, section):
        return [key[0] for key in self.omnetpp_ini_file.items(section)]

    def _has_include(self, section):
        keys = self._get_keys(section)
        for index, key in enumerate(keys):
            if key.startswith('include'):
                value = key.split()[1]
                self.omnetpp_ini_file.set(section, key, value)
                return True
        return False

    def get_section(self, section):
        return self.omnetpp_ini_file.items(section)

    def get_scenario(self, scenario, result):
        configuration = "Config " + scenario

        if any("extends" in setting for setting in self.get_section(configuration)):
            base_scenario = self.omnetpp_ini_file.get(configuration, "extends")
            # the scenario itself might be a extended scenario, so get the other settings as well
            self.get_scenario(base_scenario, result)

        for data in self.get_section(configuration):
            result[data[0]] = data[1]

        return result

if __name__ == "__main__":
    configuration = OMNeTConfigurationFileParser("/home/frey/Desktop/Projekte/code/ara-sim/simulations/ara/omnetpp.ini")
    for setting in configuration.get_section("General"):
        print((setting[0], " = ", setting[1]))

#    result = configuration.get_scenario("ARA600", {})

#    for key, value in result.items():
#        print key, " = ", value
