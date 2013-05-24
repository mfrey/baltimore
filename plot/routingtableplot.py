#!/usr/bin/env python2.7

import matplotlib.pyplot as plt

class RoutingTablePlot:
    def __init__(self):
        self.ylabel = "Pheromone value"
        self.xlabel = "Time"
        self.xlist = []
        self.ylist = []

    def draw(self, data, filename):
        plt.figure()
        plt.ylabel(self.ylabel,va="center",ha="center")
        plt.xlabel(self.xlabel)
        plt.grid(axis="y")
        
        for tuple in data:
            timestamp = tuple[0]
            next_hops = tuple[1]
            #TODO just a test
            if '192.168.0.2' in next_hops:
                plt.plot(timestamp, next_hops['192.168.0.2'], 'bo-')
                
            #plt.plot(value, self.ylist[timestamp], drawstyle="line", marker="s", color=(0./256,55./256,108./256), lw=2.5)
        
        plt.savefig(filename)
