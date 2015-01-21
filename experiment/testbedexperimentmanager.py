#!/usr/bin/env python3

import os
import socket

from socket import error
from subprocess import call

from .testbedsetup import TestbedSetup
from .experimentmanager import ExperimentManager

class TestbedExperimentManager(ExperimentManager):
    def __init__(self, baltimore_revision, libara_revision):
        super(TestbedExperimentManager, self).__init__(baltimore_revision,
            libara_revision)

    def _meh(self):
        self.nodes = []
        self.port = 4519
        self.interface = settings['testbed_interface']
        print(self.interface)


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
    settings = {
        'ara_home' : "/home/mfrey/ara-sim",
        'cwd' : ".",
        'testbed_settings' : True,
        'testbed_interface' : "wlan0",
        'ld_library_path' : "/home/mfrey/ara-sim/src/:/home/mfrey/software/rtf/lib:$LD_LIBRARY_PATH"
    }
    manager = TestbedExperimentManager(settings)
#    manager.setup()

#    manager.shutdown("ramssys")
