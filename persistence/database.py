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

    def add_experiment(self, experiment):
	data = json.loads(experiment)
        self.database['experiments'].insert(data)
      
if __name__ == "__main__":
     database = Database("baltimore_admin", "<add password>", "baltimore", "localhost")
     database.open()

