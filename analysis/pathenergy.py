#!/usr/bin/env python2.7

class PathEnergy:
    def __init__(self, node, timestamp_list, energy_list):
        self.node = node
        self.timestamp = timestamp_list
        self.energy = energy_list

    def get_index_timestamp(self, timestamp):
        try:
            index = self.timestamp.index(timestamp)
            return index
        except ValueError:
            print "no such timestamp ", timestamp
            return -1

    def get_previous_timestamp(self, timestamp):
        try:
            index = self.timestamp.index(timestamp)-1
            if index <= 0:
                print "timestamp ", timestamp, " is first timestamp"
                return -2
            return index
        except ValueError:
            print "no such timestamp ", timestamp
            return -1

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

    def size(self):
        return len(self.timestamp)

    def get_energy(self, timestamp):
        index = self.timestamp.index(timestamp)
        return self.energy[index]

    def get_timestamp(self, energy):
        index = self.energy.index(timestamp)
        return self.timestamp[index]

    def __str__(self):
        result = self.node + '\n'
        result = result + str(self.timestamp) + '\n'
        result = result + str(self.energy) 
        return result

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.timestamp)
