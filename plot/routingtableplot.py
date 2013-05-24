#!/usr/bin/env python2.7

import matplotlib.pyplot as plt

class RoutingTablePlot:
    
    def draw(self, data, filename):
        plt.figure()
        plt.ylabel("Pheromone value", va="center", ha="center")
        plt.xlabel("Time")
        plt.grid(axis="y")
        
        timestamps = []
        next_hop_values = {}
        zero_list = []
        
        # read in the data and sort them into different lists for each next_hop
        for tuple in data:
            timestamp = tuple[0]
            next_hops = tuple[1]
            
            for next_hop, pheromone_value in next_hops.iteritems():
                if next_hop not in next_hop_values:
                    next_hop_values[next_hop] = list(zero_list)
                    
                next_hop_values[next_hop].append(pheromone_value)
            
            timestamps.append(timestamp)
            zero_list.append(0)
        
        nr_of_x_values = len(timestamps)
        
        #  now just plot everything
        for address, values in next_hop_values.iteritems():
            # we need to fill up those lists where a next_hop has been removed
            values = values + [0] * (nr_of_x_values - len(values))
            
            plt.plot(timestamps, values, '-')
        
        plt.savefig(filename)
