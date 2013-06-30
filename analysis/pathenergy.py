#!/usr/bin/env python2.7

class PathEnergy:
    def __init__(self, node, timestamp_list, energy_list):
        self.node = node
        self.timestamp = timestamp_list
        self.energy = energy_list

    def get_next_timestamp(self, timestamp):
        try:
            index = self.timestamp.index(timestamp)

	    if index == len(self.timestamp)-1:
                print "timestamp ", timestamp, " is last timestamp"
                return -2
            return index + 1
        except ValueError:
            print "no such timestamp ", timestamp
            return -1

    def get_energy(self, timestamp):
        index = self.timestamp.index(timestamp)
        return self.energy[index]

    def get_timestamp(self, energy):
        index = self.energy.index(timestamp)
        return self.timestamp[index]

    def __str__(self):
        str = self.node + '\n'
        str = str + self.timestamp + '\n'
        str = str + self.energy 
	return str

    def __repr__(self):
        return self.__str__()
