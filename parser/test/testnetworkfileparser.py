#!/usr/bin/env python2.7

import unittest

from parser import networkfileparser as nfp

class TestNetworkFileParser(unittest.TestCase):
    def setUp(self):
        self.parser = nfp.NetworkFileParser()
        print("bla")

#    def test_read(self):
#        print "foo"
#        self.parser.read("/home/frey/results/midSize-StartPositions.txt")

if __name__ == '__main__':
    unittest.main()
