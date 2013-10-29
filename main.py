#!/usr/bin/env python2.7

import os
from os import path
import logging
import argparse

import matplotlib
matplotlib.use("Agg")

#from persistence.database import Database
from experiment.git import Git
from configuration.configuration import Configuration
from experiment.experimentmanager import ExperimentManager
from analysis.visualize import Visualize

def main():
    logger = logging.getLogger('baltimore')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
    parser.add_argument('-c', dest='configuration', type=str, default="", action='store', help='a configuarion file for baltimore')
    parser.add_argument('-d', dest='directory', type=str, default="", action='store', help='a directory which contains OMNeT++ result files')
    parser.add_argument('-s', dest='scenario', type=str, default="", action='store', help="evaluate a specific scenario")
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, const=True, action='store_const', help="print out verbose information for each iteration")
    parser.add_argument('-r', '--run', dest='run', default=False, const=True, action='store_const', help="first run the simulations as specified via the configuration then analyse the results")
    parser.add_argument('-t', '--testbed', dest='testbed', default=False, const=True, action='store_const', help="run a testbed experiment")
    parser.add_argument('-p', '--plot', dest='plot', default=False, const=True, action='store_const', help="draw graphs")
    parser.add_argument('-e', '--evaluate', dest='evaluate', default=False, const=True, action='store_const', help="evaluate results")
    parser.add_argument('-o', '--analyze-other-protocol', dest='analyze_other_protocol', default=False, const=True, action='store_const', help="Run analysis for other MANET routing protocol (like results for AODV, DSR or DSDV)")
    
    arguments = parser.parse_args()

    configuration = get_configuration(arguments)
    git = Git()

    baltimore_revision = git.get_revision(".")
    libara_revision = git.get_revision(configuration.settings['ara_home'])

    check_matplotlibrc_support(configuration.settings)

    if arguments.run == True and arguments.testbed == False:
        experiment_manager = ExperimentManager(baltimore_revision, libara_revision)
        run_simulation(configuration.settings, experiment_manager)
        evaluate_simulation(configuration.settings, experiment_manager, arguments)

    elif arguments.run == False and arguments.testbed == True:
        run_testbed(configuration)

    elif arguments.run == False and arguments.testbed == False:
        if arguments.evaluate == True:
            experiment_manager = ExperimentManager(baltimore_revision, libara_revision)
            evaluate_simulation(configuration.settings, experiment_manager, arguments)

        if arguments.plot == True:
            visualize = Visualize(configuration.settings)
    else:
        print "at present you can't run testbed and simulation experiments at the same time"
    

def check_matplotlibrc_support(configuration):
    rc_file = configuration['analysis_matplotlib']
    if rc_file != "":
        matplotlib.rc_file(path.expanduser(rc_file))


def run_simulation(settings, experiment_manager):
    experiment_manager.result_dir_exists(settings['cwd'])
    experiment_manager.check_result_directory(settings['cwd'] + '/results', settings['scenarios'])
    experiment_manager.run_simulations(settings)


def evaluate_simulation(settings, experiment_manager, arguments):
    for scenario in settings['experiments']:
         scenario_home = scenario[1]
         remaining_scenarios = experiment_manager.check_result_files(settings['cwd'] + '/' + scenario[0] + '/results', scenario[2])
         settings['scenarios'] = remaining_scenarios
         experiment_manager.process(settings, arguments)


    remaining_scenarios = experiment_manager.check_result_files(settings['cwd'] + '/results', settings['scenarios'])
    settings['scenarios'] = remaining_scenarios
    experiment_manager.process(settings, arguments)

#    if settings['database_settings']:
#        store_experiment_results(settings, experiment_manager)


#def store_experiment_results(settings, experiment_manager):
 #   database = Database(settings['database_user'], settings['database_password'], settings['database_db'], settings['database_host'])
#    database.open()
#    database.add_experiment(experiment_manager)
#    database.close()


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
