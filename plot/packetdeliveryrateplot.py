#!/usr/bin/env python2.7

class PacketDeliveryRatePlot:
  def draw(self, filename):
	plt.figure()
	plt.plot([0,10,50,80,90,100], [10,10,8,7,6,0], drawstyle="steps", color=(0./256,55./256,108./256), lw=2.5)
	#plt.axis([0, 110, 0, 11])
	plt.ylabelself.ylabel,va="center",ha="center")
	plt.xlabel(self.xlabel)
	plt.savefig(filename)

  def __init__(self):
	self.ylabel = "Delivery Rate [%]"
	self.xlabel = "Pause Time [sec]"




