#!/usr/bin/env python2.7

import argparse

from parser.routingtabledataparser import RoutingTableDataParser
from plot.routingtableplot import RoutingTablePlot

def main():
    parser = argparse.ArgumentParser(description='foo')
    parser.add_argument('-f', dest='file', type=str, default="../ARA-Simulation/simulations/mobile/results/smallMobile-0-node0.rtd", action='store')
    arguments = parser.parse_args()
    
    parser = RoutingTableDataParser()
    data = parser.read_data_from(arguments.file, "192.168.0.2")
    plot = RoutingTablePlot()
    plot.draw(data, "test.png")
        
if __name__ == "__main__":
    main()
