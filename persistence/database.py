#!/usr/bin/env python2.7

from pymongo import MongoClient

class Database:
    def __init__(self, user, password, host, database):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
   
#    def add_experiment(self, experiment):
        
