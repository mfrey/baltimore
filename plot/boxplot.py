#!/usr/bin/env python2.7

#from pylab import rand, ones, concatenate
import matplotlib.pyplot as plt

class BoxPlot:
    def __init__(self):
        self.ylabel = ""
        self.xlabel = ""
        self.xticklabels = []
        self.ylist = []

    def draw(self, data, filename):
        figure = plt.figure()
        plt.boxplot(data)
        plt.ylabel(self.ylabel,va="center",ha="center")
        plt.xlabel(self.xlabel)
        plt.grid(axis="y")
        plt.savefig(filename)
        plt.close()

#if __name__ == "__main__":
#    spread= rand(50) * 100
#    center = ones(25) * 50
#    flier_high = rand(10) * 100 + 100
#    flier_low = rand(10) * -100
#    data =concatenate((spread, center, flier_high, flier_low), 0)

#    plot = BoxPlot()
#    plot.draw(data, "test.png")
