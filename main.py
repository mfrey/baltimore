#!/usr/bin/env python2.7

import os
import sys
import argparse

import matplotlib
matplotlib.use("Agg")

from persistence.database import Database
from experiment.git import Git
from configuration.configuration import Configuration
from experiment.experimentmanager import ExperimentManager

def main():
    parser = argparse.ArgumentParser(description='baltimore - an evaluation script for the ara-sim framework')
    parser.add_argument('-c', dest='configuration', type=str, default="", action='store', help='a configuarion file for baltimore')
    parser.add_argument('-d', dest='directory', type=str, default="", action='store', help='a directory which contains OMNeT++ result files')
    parser.add_argument('-s', dest='scenario', type=str, default="", action='store', help="evaluate a specific scenario")
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, const=True, action='store_const', help="print out verbose information for each iteration")
    parser.add_argument('-j', '--json-write', dest='json_write', type=str, default="", action='store', help="specify location for json export")
    parser.add_argument('-J', '--json-read', dest='json_read', type=str, default="", action='store', help="specify location for json import")
    parser.add_argument('-r', '--run', dest='run', default=False, const=True, action='store_const', help="first run the simulations as specified via the configuration then analyse the results")
    arguments = parser.parse_args()

    configuration = get_configuration(arguments)
    git = Git()

    baltimore_revision = git.get_revision(".")
    libara_revision = git.get_revision(configuration.settings['ara_home'])

    experiment_manager = ExperimentManager(baltimore_revision, libara_revision)

    if arguments.run == True:
        experiment_manager.result_dir_exists(configuration.settings['cwd'])
        # check if there are already files from past runs in the directory
        experiment_manager.check_result_directory(configuration.settings['cwd'] + '/results', configuration.settings['scenarios'])
        experiment_manager.run_simulations(configuration.settings)

    remaining_scenarios = experiment_manager.check_result_files(configuration.settings['cwd'] + '/results', configuration.settings['scenarios'])
    configuration.settings['scenarios'] = remaining_scenarios

    experiment_manager.process(configuration.settings, arguments.verbose)

    if arguments.json_write != "":
        experiment_manager.write_json(arguments.json_write)

    if arguments.json_read != "":
        experiment_manager.read_json(arguments.json_read)

    if configuration.settings['db_settings']:
        database = setup_database_connection(configuration.settings)
        # database.add_experiment(experiment_manager.create_json())
        database.close()

def setup_database_connection(settings):
    database = Database(settings['db_user'], settings['db_password'], settings['db_db'], settings['db_host'])
    database.open()
    return database

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
