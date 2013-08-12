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
        self.legend_location = 2
        self.labels = []
        self.markers = ['s','^','v','2','*','3','d']

    def draw(self, filename):
        figure = plt.figure()
        ax = figure.add_subplot(111)
        for index, value in enumerate(self.xlist):
            if len(self.xlist) > 1:
                plt.plot(value, self.ylist[index], drawstyle="line", marker=self.markers[index], lw=2.5, label=self.labels[index])
            else:
                plt.plot(value, self.ylist[index], drawstyle="line", marker=self.markers[index], lw=2.5)

        plt.ylabel(self.ylabel,va="center",ha="center")
        plt.xlabel(self.xlabel)
        plt.title(self.title)

        plt.yticks(self.yticks)
        plt.xticks(self.xlist[0], rotation=45)

        if len(self.xlist) > 1:
            plt.legend(loc=self.legend_location)

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
