#!/usr/bin/env python2.7

import unittest

from representation.scalarfile import scalarfile as scalar

class TestScalarFile(unittest.TestCase):
  def setUp(self):
    self.scalarFile = scalar.ScalarFile() 

if __name__ == '__main__':
    unittest.main()


