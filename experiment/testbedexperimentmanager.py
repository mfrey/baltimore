#!/usr/bin/env python2.7

from socket import error

class TestbedExperimentManager:
    def __init__(self):
        self.nodes = []
        self.port = 4519

   def setup(self): 
       raise "not yet implemented"

   def shutdown(self): 
       raise "not yet implemented"

   def _setup_interfaces(self):
       raise "not yet implemented"

if __name__ == "__main__":
    manager = TestbedExperimentManager()
#    manager.shutdown("ramssys")

