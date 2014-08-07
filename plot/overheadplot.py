#!/usr/bin/env python3

import os
import re
import csv
import numpy as np
import matplotlib.pyplot as plt

import json
import requests
import matplotlib

class OverheadPlot:
    def __init__(self):
        self.title = "Overhead ($\mu$ and $\pm \sigma$ interval)"
        self.ylabel = "Packets [%]"
        self.xlabel = "Pause Time [s]"
        self.xlist = []
        self.mu = []
        self.sigma = []
        #self.yticks = [2, 3, 4, 6, 7, 8, 9, 10, 12, 15]
        #self.yticks = [0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0]
        self.yticks = [2, 3, 4, 6, 7, 8, 9, 10]
        self.labels = []
        self.markers = ['s','^','v','2','*','3','d']
        self.legend_location = 4

    def draw(self, filename):
        figure, axis = plt.subplots(1)
        axis.plot(self.xlist, self.mu, lw=2, label='ARA', color='#348ABD')
 #       axis.plot(t, mu1, lw=2, label='mean population 2', color='yellow')
        #axis.fill_between(self.xlist, self.mu + self.sigma, self.mu - self.sigma, facecolor='blue', alpha=0.5)
        axis.fill_between(self.xlist, [i + j for i, j in zip(self.mu, self.sigma)], [i - j for i, j in zip(self.mu, self.sigma)], facecolor='#348ABD', alpha=0.5)
#        axis.fill_between(t, mu2+sigma2, mu2-sigma2, facecolor='yellow', alpha=0.5)
        axis.set_title(self.title)
        axis.legend(loc=self.legend_location)
        axis.set_xlabel(self.xlabel)
        axis.set_ylabel(self.ylabel)
        axis.grid()
        figure.savefig(filename)

if __name__ == "__main__":
    csv_location = '/home/michael/Desktop/Projekte/remote/jupiter/Desktop/TechReport' 

    overhead = {}
    scenarios = ['ARA0', 'ARA100', 'ARA300', 'ARA500', 'ARA700', 'ARA900', 'ARA1000'] 
    scenario_files = {}

    for root, _, files in os.walk(csv_location):
        for name in files:
            if name.endswith('csv'):
                scenario = name.split("/")[-1].split("_")[0]
                if scenario in scenarios:
                    if scenario not in scenario_files:
                       scenario_files[scenario] = []
                    scenario_files[scenario].append(os.path.join(root, name))

    for scenario in scenario_files:
        for csv_file in scenario_files[scenario]:
            if csv_file.endswith("overhead_raw.csv"):
                overhead[scenario] = []
                with open(csv_file, 'rt') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    next(reader)

                    for row in reader:
                        if len(row) > 1:
                            overhead[scenario].append(float(row[1]) * 100)

#                print(overhead[scenario])
#                print("                ")

#    print(overhead)
    s = requests.get("https://raw.github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/master/styles/bmh_matplotlibrc.json").json()
    matplotlib.rcParams.update(s)


    plot = OverheadPlot()
    plot.xlist = [0, 100, 300, 500, 700, 900, 1000]

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    
    mean = []
    std = []

    for scenario in sorted(overhead, key = alphanum_key):
        mean.append(np.mean(overhead[scenario]))
        std.append(np.std(overhead[scenario]))

    plot.mu = mean
    plot.sigma = std
    plot.draw("test.pdf")
