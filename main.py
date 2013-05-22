#!/usr/bin/env python2.7

import sys
import argparse

from configuration.configuration import Configuration
from experiment.experimentmanager import ExperimentManager

def main():
    parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
    parser.add_argument('-d', dest='directory', type=str, default=".", action='store', help='a directory which contains OMNeT++ result files')
    parser.add_argument('-c', dest='configuration', type=str, default="", action='store', help='a configuarion file for baltimore')
    parser.add_argument('-v', dest='verbose', default=False, const=True, action='store_const', help="print out verbose information for each iteration")
    parser.add_argument('-n', dest='network', default=False, const=True, action='store_const', help="draw network graph for scenario(s)")
    parser.add_argument('-s', dest='scenario', type=str, default="", action='store', help="evaluate a specific scenario")
    parser.add_argument('-j', dest='json', type=str, default="", action='store', help="specify location for json export")
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
      parser.print_help()
      sys.exit(1)

    experiment_manager = ExperimentManager()

    # check if the argument has been set 
#    if arguments.configuration.endswith("ini"):
#      configuration = Configuration(arguments.configuration)
#      experiment_manager.run_simulations(configuration.settings)

    experiment_manager.process(arguments.directory, arguments.scenario, arguments.verbose, arguments.network)


if __name__ == "__main__":
    main()
