#!/usr/bin/env python2.7

import argparse
from experiment.experimentmanager import ExperimentManager

def main():
    parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
    parser.add_argument('-d', dest='directory', type=str, default=".", action='store', help='a directory which contains OMNeT++ result files')
    parser.add_argument('-v', dest='verbose', default=False, const=True, action='store_const', help="print out verbose information for each iteration")
    parser.add_argument('-n', dest='network', default=False, const=True, action='store_const', help="draw network graph ")
    parser.add_argument('-s', dest='scenario', type=str, default="", action='store', help="evaluate a specific scenario")
    arguments = parser.parse_args()
    
    experiment_manager = ExperimentManager()
    experiment_manager.process(arguments.directory, arguments.scenario, arguments.verbose, arguments.network)

if __name__ == "__main__":
    main()
