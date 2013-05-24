#!/usr/bin/env python2.7

import argparse

from os.path import basename
from parser.routingtabledataparser import RoutingTableDataParser
from plot.routingtableplot import RoutingTablePlot

def main():
    parser = argparse.ArgumentParser(description='foo')
    parser.add_argument('-f', dest='file', type=str, default="../ara-sim/simulations/static/results/bigStatic-0-node16.rtd", action='store')
    arguments = parser.parse_args()
    filename = basename(arguments.file) + '.png'

    parser = RoutingTableDataParser()
    data = parser.read_data_from(arguments.file, "192.168.0.8")
    plot = RoutingTablePlot()
    plot.draw(data, filename)
        
if __name__ == "__main__":
    main()
