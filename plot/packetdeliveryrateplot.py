#!/usr/bin/env python2.7

import matplotlib.pyplot as plt

class PacketDeliveryRatePlot:
  def __init__(self):
	self.ylabel = "Delivery Rate [%]"
	self.xlabel = "Pause Time [sec]"
        self.xlist = []
        self.ylist = []


  def draw(self, filename):
	plt.figure()
        for index, value in enumerate(self.xlist):
	  plt.plot(value, self.ylist[index], drawstyle="line", marker="s", color=(0./256,55./256,108./256), lw=2.5)
	plt.ylabel(self.ylabel,va="center",ha="center")
	plt.xlabel(self.xlabel)
	plt.grid(axis="y")
	plt.savefig('test.png')


foo = PacketDeliveryRatePlot()
foo.test()


