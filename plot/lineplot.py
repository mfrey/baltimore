#!/usr/bin/env python2.7

import matplotlib.pyplot as plt

class LinePlot:
    def __init__(self):
        self.ylabel = ""
        self.xlabel = ""
        self.xticks = []
        self.yticks = []
        self.xticklabels = []
        self.xlist = []
        self.ylist = []
        self.title = ""

    def draw(self, xdata, ydata, filename):
        figure = plt.figure()
        plt.plot(xdata, ydata)
        plt.ylabel(self.ylabel,va="center",ha="center")
        plt.xlabel(self.xlabel)
        plt.title(self.title)

        if len(self.yticks) != 0:
           plt.yticks(self.yticks)
        if len(self.xticks) != 0:
           plt.xticks(self.xticks)

        plt.grid(axis="y")
        plt.savefig(filename)
        plt.close()

#if __name__ == "__main__":
#    spread= rand(50) * 100
#    center = ones(25) * 50
#    flier_high = rand(10) * 100 + 100
#    flier_low = rand(10) * -100
#    data =concatenate((spread, center, flier_high, flier_low), 0)

#    plot = LinePlot()
#    plot.draw(data, "test.png")
