#!/usr/bin/env python2.7

import argparse

from experiment import experiment as exp
from representation import scalarfile as scalar
from analysis import packetdeliveryrateanalysis as pdr
from configuration import configuration as cfg

def main():
    parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
    parser.add_argument('-d', dest='directory', type=str, default=".", action='store', help='a directory which contains OMNeT++ result files')
    parser.add_argument('-v', dest='verbose', default=False, const=True, action='store_const', help="print out verbose information for each iteration")
    parser.add_argument('-s', dest='scenario', type=str, default="", action='store', help="evaluate a specific scenario")
    arguments = parser.parse_args()
    
    experiment = exp.Experiment(arguments.directory+'/results', 'midSizeScenario')
    experiment.get_results()
    #experiment_manager = expm.ExperimentManager()
    #experiment_manager.read_directory(arguments.directory, arguments.scenario)
    #experiment_manager.evaluate(arguments.verbose)  

if __name__ == "__main__":
    main()
