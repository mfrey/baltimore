#!/usr/bin/env python2.7

import numpy as np
import matplotlib.pyplot as plt

class PacketDeliveryRatePlot:
    def __init__(self):
        self.title = "Packet Delivery Rate (Average)"
        self.ylabel = "Delivery Rate [%]"
        self.xlabel = "Pause Time [sec]"
        self.xlist = []
        self.ylist = []
        self.yticks = [20, 30, 40, 60, 70, 80, 90, 100]
        self.labels = []
        self.markers = ['s','^','v','2','*','3','d']

    def draw(self, filename):
        figure = plt.figure()
        ax = figure.add_subplot(111)
        for index, value in enumerate(self.xlist):
            #plt.plot(value, self.ylist[index], drawstyle="line", marker="s", color=(0./256,55./256,108./256), lw=2.5)
            if len(self.xlist) > 1:
                plt.plot(value, self.ylist[index], drawstyle="line", marker=self.markers[index], lw=2.5, label=self.labels[index])
            else:
                plt.plot(value, self.ylist[index], drawstyle="line", marker=self.markers[index], lw=2.5)
        plt.ylabel(self.ylabel,va="center",ha="center")

        plt.yticks(self.yticks)
        plt.xticks(self.xlist[0])
        plt.xlabel(self.xlabel)
        plt.title(self.title)
        if len(self.xlist) > 1:
            plt.legend()
        plt.grid(axis="y")
        plt.savefig(filename)
        plt.close()

if __name__ == "__main__":
    xlist = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    ylist = [[95,80,75,90],[90,85,70,93], [93,87,75,90], [90,89,60,91]]
    plot = PacketDeliveryRatePlot()
    plot.xlist = xlist
    plot.ylist = ylist
    plot.draw("test.png")
