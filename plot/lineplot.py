#!/usr/bin/env python2.7

import csv
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
                #plt.plot(value, self.ylist[index], drawstyle="line", marker=self.markers[index], lw=2.5, label=self.labels[index])
                plt.plot(value, self.ylist[index], drawstyle="line", lw=2.5, label=self.labels[index])
            else:
                plt.plot(value, self.ylist[index], drawstyle="line", marker=self.markers[index], lw=2.5)

        ylabel = plt.ylabel(self.ylabel,va="center",ha="center")
        xlabel = plt.xlabel(self.xlabel)
        #print xlabel.get_position()
        plt.title(self.title)

        plt.yticks(self.yticks)
        #plt.xticks(self.xlist[0], rotation=45)
        plt.xticks(self.xticks)

        if len(self.xlist) > 1:
            plt.legend(loc=self.legend_location)

        plt.grid(axis="y")
        xlabel.set_position((0.5, 0.1))
        ylabel.set_position((5, 0.5))
        plt.savefig(filename)
        plt.close()

if __name__ == "__main__":
    plot = LinePlot()

    result = []

    with open('expected_pheromone_values_table.dat', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='"')
        for row in reader:
            row = filter(lambda a: a != '', row)
            result.append(row)
    
    result.pop(0)
    plot.labels = ['1.0', '0.5', '0.25']
    xlist = [float(row[0]) for row in result] 

    for i in range(3):
        plot.xlist.append(xlist)

    plot.ylist = [[] for i in range(3)]

    for row in result:
        plot.ylist[0].append(float(row[1]))
        plot.ylist[1].append(float(row[3]))
        plot.ylist[2].append(float(row[2]))

    plot.title = "Pheromone Evolution"
    plot.xticks = [0, 5, 10, 15]
    plot.yticks = [0, 100, 200]
    plot.xlabel = "Time [s]"
    plot.ylabel = "Pheromones"

    plot.draw("test.pdf")
