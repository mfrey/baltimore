#!/usr/bin/env python2.7

from socket import error
from experiment import TestbedSetup

class TestbedExperimentManager:
    def __init__(self, interface):
        self.nodes = []
        self.port = 4519
        self.interface = interface

   def setup(self):
       self._setup_interfaces()

   def shutdown(self): 
       raise "not yet implemented"

   def _setup_interfaces(self):
       setup = TestbedSetup(self.interface)
       setup.set_up_interface()

if __name__ == "__main__":
    manager = TestbedExperimentManager()
#    manager.shutdown("ramssys")

