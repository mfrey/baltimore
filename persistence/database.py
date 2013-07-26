#!/usr/bin/env python2.7

import json

from pymongo import MongoClient
from pymongo.errors import PyMongoError

class Database:
    def __init__(self, user, password, database, host, port=27017):
        self.user = user
        self.password = password
        self.database_name = database
        self.host = host
        self.port = port

    def open(self):
        self.client = MongoClient(self.host, self.port)
        self.database = self.client[self.database_name]
        try:
            self.database.authenticate(self.user, self.password)
        except PyMongoError: 
            print "user and/or password unknown"
 
    def close(self):
        self.client.close()

    def add_experiment(self, experiment, scenarios, omnetpp_ini_checksum, standard_ini_checksum):
        for scenario in scenarios:
            if experiment_exists(scenario, omnetpp_ini_checksum, standard_ini_checksum):
                # remove the scenario from list

        #if len(experiment.scenarios) > 0:
        #    data = json.loads(experiment)
        #    self.database['experiments'].insert(data)

    def experiment_exists(self, scenario, omnetpp_ini_checksum, standard_ini_checksum):
        experiments = self.database['experiments']
        result = experiments.find({ "experiments." + scenario : { "$exists": True}, "omnetpp_ini_checksum" : omnetpp_ini_checksum, "standard_ini_checksum" : standard_ini_checksum}).count()
        return result != 0
      
if __name__ == "__main__":
     database = Database("baltimore_admin", "<add password>", "baltimore", "localhost")
     database.open()

