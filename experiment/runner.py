#!/usr/bin/env python2.7

import os

from subprocess import call

def run_simulation(args):
    return Runner(*args).run()

class Runner(object):
    def __init__(self, scenario, repetition, settings):
        self.scenario = scenario
        self.repetition = repetition
        self.ned_path = settings['ned_path']
        self.omnetpp_ini = settings['omnetpp_ini']
        self.binary = settings['ara_home'] + '/omnetpp/ara-sim'
        self.ld_library_path = settings['ld_library_path']
        self.cwd = settings['cwd']
        self.total_nr_of_runs = settings['repetitions']

        if os.path.exists(self.binary) == False:
            raise Exception("The ara-sim binary could not be found at path" + self.binary)

    def run(self):
        environment = dict(os.environ)
        environment['LD_LIBRARY_PATH'] = self.ld_library_path
        logfile_path = self.cwd + 'results/' + self.scenario + '-' + str(self.repetition) + '-Log.txt'

        with open(logfile_path, 'w') as logfile:
            print "Running [" + self.scenario + "] " + str(self.repetition+1) + "/" + str(self.total_nr_of_runs) + ": Log is saved to " + logfile_path
            call([self.binary, "-r", str(self.repetition), "-u", "Cmdenv", "-c", self.scenario, "-n", self.ned_path, self.omnetpp_ini], env=environment, cwd=self.cwd, stdout=logfile)
