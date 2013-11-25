#!/usr/bin/env python3

import os
import socket

from socket import error
from subprocess import call

from experiment import TestbedSetup

class TestbedExperimentManager:
    def __init__(self, settings):
        self.nodes = []
        self.port = 4519
        self.interface = settings['testbed_interface'] 

        self.binary = settings['ara_home'] + '/testbed/des-ara.init'
        self.ld_library_path = settings['ld_library_path']
        self.cwd = settings['cwd']

        self.environment = dict(os.environ)
        self.environment['LD_LIBRARY_PATH'] = self.ld_library_path

    def setup(self):
        self._setup_interfaces()

        hostname = socket.gethostname()

        # TODO: fixit
        logfile_path = self.cwd + '/' + hostname + '-Log.txt'

        with open(logfile_path, 'w') as logfile:
            call([self.binary, "start"], env=self.environment, cwd=self.cwd, stdout=logfile)

    def shutdown(self): 
        call([self.binary, "stop"], env=self.environment, cwd=self.cwd)

    def _setup_interfaces(self):
        setup = TestbedSetup(self.interface)
        setup.set_up_interface()

if __name__ == "__main__":
    manager = TestbedExperimentManager()
#    manager.shutdown("ramssys")

