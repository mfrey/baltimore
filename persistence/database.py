#!/usr/bin/env python3

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
            print("user and/or password unknown")
 
    def close(self):
        self.client.close()

    def add_experiment(self, experiment_manager):
        omnetpp_ini_checksum = experiment_manager.omnetpp_ini_checksum
        standard_ini_checksum = experiment_manager.standard_ini_checksum
        scenarios = []

        for scenario in experiment_manager.experiments:
            if self.experiment_exists(scenario, omnetpp_ini_checksum, standard_ini_checksum):
                # store scenarios which will be removed
                scenarios.append(scenario)

        # remove already existing entries
        for scenario in scenarios:
            del experiment_manager.experiments[scenario]

        if len(experiment_manager.experiments) > 0:
            data = json.loads(experiment_manager.create_json())
            self.database['experiments'].insert(data)

    def experiment_exists(self, scenario, omnetpp_ini_checksum, standard_ini_checksum):
        experiments = self.database['experiments']
        result = experiments.find({ "experiments." + scenario : { "$exists": True}, "omnetpp_ini_checksum" : omnetpp_ini_checksum, "standard_ini_checksum" : standard_ini_checksum}).count()
#DEBUG:        print "experiments.find({ experiments." + scenario + ": { $exists : True},  omnetpp_ini_checksum : " + omnetpp_ini_checksum + ", standard_ini_checksum : " + standard_ini_checksum + "}).count()"
        return result != 0
      
if __name__ == "__main__":
     database = Database("baltimore_admin", "<add password>", "baltimore", "localhost")
     database.open()

