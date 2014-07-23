#!/usr/bin/env python3

import matplotlib.pyplot as plt

class BarChart:
    def __init__(self):
        self.ylabel = ""
        self.xlabel = ""
        self.xticks = []
        self.yticks = []
        self.xticklabels = []
        self.xlist = []
        self.ylist = []
        self.title = ""
        self.bar_widths = -1;

    def draw(self, xdata, ydata, filename):
        figure = plt.figure()

        if self.bar_widths > 0:
            plt.bar(xdata, ydata, self.bar_widths)
        else:
            plt.bar(xdata, ydata)

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
