# -*- coding: UTF-8 -*-

import yaml
import urllib
import csv

import logging


class AuthConnector:

    def __init__ (self,config, logger):
        self.config = config
        self.logger = logger
        
        # Set a couple of default values
        self.config['delimiter'] = config['delimiter'] if conf.has_key('delimiter') else ','
        self.config['quotechar'] = config['quotechar'] if conf.has_key('quotechar') else '|'

        #print "Not implemented yet"
        #return None

    def search(self,dni):
        
        # Loads the data, in csv
        authfile = urllib(self.config.get('uri')).readlines()
        
        reader = csv.reader(authfile,\
         delimiter=config['delimiter'], quotechar=config['quotechar'])
            
        # There has to be a better way of doing this...
        users = [row for row in reader if dni in row]
        
        return len(users) != 0
