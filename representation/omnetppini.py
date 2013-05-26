#!/usr/bin/env python2.7

import ConfigParser

class OMNeTConfiguration:
    def __init__(self, file_name):
        self.omnetpp_ini_file = ConfigParser.ConfigParser()
	self.omnetpp_ini_file.read(file_name)

    def get_section(self, section):
        return self.omnetpp_ini_file.items(section)

    def get_scenario(self, scenario):
        return self.get_section("Config " + scenario)

if __name__ == "__main__":
     configuration = OMNeTConfiguration("/vol/home-vol1/simulant/frey/Desktop/Projekte/code/ara-sim/simulations/static/omnetpp.ini")
     for setting in configuration.get_section("General"):
         print setting[0], " = ", setting[1]

     for setting in configuration.get_scenario("midStatic"):
         print setting[0], " = ", setting[1]
