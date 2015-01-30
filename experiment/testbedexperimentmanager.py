#!/usr/bin/env python2.7

import os
import socket

from socket import error
#from subprocess import call, Popen
import subprocess  

from .testbedsetup import TestbedSetup
from .experimentmanager import ExperimentManager

class TestbedExperimentManager(ExperimentManager):
    def __init__(self, baltimore_revision, libara_revision):
        super(TestbedExperimentManager, self).__init__(baltimore_revision,
            libara_revision)

    def _initialize(self, settings):
        # port of the routing daemon management interface
        self.port = 4519
        # nodes which are part of the experiment
        self.nodes = settings['testbed_nodes']

        # default interface of the routing daemon
        self.interface = settings['testbed_interface']
        # 
        self.binary = settings['ara_home'] + '/testbed/des-ara.init'
        self.ld_library_path = settings['ld_library_path']
        self.cwd = settings['cwd']

        self.environment = dict(os.environ)
        self.environment['LD_LIBRARY_PATH'] = self.ld_library_path


        self._write_nodes_file()
        self._pre()

    def _write_nodes_file(self):
        assert len(self.nodes) > 0
        self.nodes_file = "/tmp/" + "nodes-" + str(os.getpid()) + ".txt"
        with open(self.nodes_file, 'w') as node_file:
            for node in self.nodes:
                node_file.write(node.strip() + "\n")

    def _pre(self):
        # setup interfaces for each node
        setup = TestbedSetup(self.interface)
        with open("/tmp/testcommand.txt", 'w') as logfile:
            for command in setup.commands:
                print(command)
                #call(["parallel-ssh", "-h", self.nodes_file, "-l", "root", "-i", command], env=self.environment, cwd=self.cwd, stdout=logfile)
                # TODO would be nice if we could avoid the shell option
                pipe = subprocess.Popen(["parallel-ssh", "-h", self.nodes_file, "-l", "root", "-A", "-i", command], env=self.environment, cwd=self.cwd, stdin=subprocess.PIPE, stdout=logfile, shell=True)
                # TODO should also try to avoid to write hte passwort somewhere
                # (the real testbed actually uses ssh keys, while the testbed
                # test # routers ask for a password)
                print(pipe.communicate(bytes("that's uncool\n", 'UTF-8')))


    def run_testbed_experiments(self, settings):
        self._initialize(settings)

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
