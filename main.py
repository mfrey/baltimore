#!/usr/bin/env python2.7

import os
import sys
import argparse

import matplotlib
matplotlib.use("Agg")

from configuration.configuration import Configuration
from experiment.experimentmanager import ExperimentManager

def main():
    parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
    parser.add_argument('-c', dest='configuration', type=str, default="", action='store', help='a configuarion file for baltimore')
    parser.add_argument('-d', dest='directory', type=str, default="", action='store', help='a directory which contains OMNeT++ result files')
    parser.add_argument('-s', dest='scenario', type=str, default="", action='store', help="evaluate a specific scenario")
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, const=True, action='store_const', help="print out verbose information for each iteration")
    parser.add_argument('-n', '--network', dest='network', default=False, const=True, action='store_const', help="draw network graph for scenario(s)")
    parser.add_argument('-j', '--json', dest='json', type=str, default="", action='store', help="specify location for json export")
    parser.add_argument('-r', '--run', dest='run', default=False, const=True, action='store_const', help="first run the simulations as specified via the configuration then analyse the results")
    arguments = parser.parse_args()

    configuration = get_configuration(arguments)

    experiment_manager = ExperimentManager()
	# check if there are already files from past runs in the directory
    experiment_manager.check(configuration.settings['cwd'] + '/results', configuration.settinsg['scenarios'])

    if arguments.run == True:
        experiment_manager.run_simulations(configuration.settings)
    
    experiment_manager.process(configuration.settings['cwd'], configuration.settings['scenarios'], arguments.verbose, arguments.network)

def get_configuration(arguments):
    if arguments.configuration != "":
        print "Reading configuration from", arguments.configuration
        configuration = Configuration(arguments.configuration)
    elif os.path.exists('baltimore.ini'):
        print "Using standard configuration: ./baltimore.ini"
        configuration = Configuration('baltimore.ini')
    else:
        configuration = Configuration.createDefaultConfiguration()
    
    if arguments.directory != "":
        configuration.settings['cwd'] = arguments.directory
    
    if arguments.scenario != "":
        configuration.settings['scenarios'] = [arguments.scenario]
    
    if configuration.settings['cwd'].endswith('/') == False:
        configuration.settings['cwd'] += '/'
    
    return configuration

if __name__ == "__main__":
    main()
