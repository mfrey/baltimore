#!/usr/bin/env python2.7

import ConfigParser

class OMNeTConfigurationFileParser:
    def __init__(self, file_name):
        self.omnetpp_ini_file = ConfigParser.ConfigParser()
        self.omnetpp_ini_file.read(file_name)

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
        print setting[0], " = ", setting[1]

    result = configuration.get_scenario("ARA600", {})

    for key, value in result.items():
        print key, " = ", value
