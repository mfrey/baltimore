#!/usr/bin/env python2.7

import unittest

from representation import scalarfile as scalar

class TestScalarFile(unittest.TestCase):
  def setUp(self):
    self.scalarFile = scalar.ScalarFile() 

  def test_get_node_identifier():
    test_string = "scalar Scenario05.node[0].app 	trafficSent 	0" 
    self.assertIs(self.scalarFile.get_node_identifier(test_string), 0)

if __name__ == '__main__':
    unittest.main()


