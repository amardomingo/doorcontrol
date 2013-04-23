#!/usr/bin/python -tt
# -*- coding: UTF-8 -*-

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), 'parallel/'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'serial'))
sys.path.append(os.path.join(os.path.dirname(__file__), './raspberry'))

import string
import time
import logging
import yaml
import re

import LdapConnector

from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.util import toASCIIString
from smartcard.CardMonitoring import CardMonitor, CardObserver

class DoorListener( CardObserver ):

    def __init__ (self,ldap_connector, config_path, logger):
        """
        Initializes the door_listener
        As parameters, it needs the ldap connector to the
        ldap where the user data is stored, the path to the config
        file with the parameters for the port, and a logger
        """
        self.ldap = ldap_connector
        self.config = self.load_config(config_path)
        self.logger = logger

        
        #Select the card port
        if (self.config['parallel']['use']):
            import door.parallel as Door
            self.door_handler = Door.Door(self.config['parallel'], self.logger)
        elif (self.config['serial']['use']):
            import door.serial as  Door
            self.door_handler = Door.Door(self.config['serial'], self.logger)
        elif (self.config['raspberry']['use']):
            print 'importing raspberry'
            import door.raspberry as Door
            print 'imported'
            self.door_handler = Door.Door(self.config['raspberry'], self.logger)
        else:
            logger.error("cannot recognize configuration")
            sys.exit()
        

    # Method to be added to the observer
    def update(self, observable, (addedcards, removedcards)):
        """
        Method called when a card is inserted or removed from the card reader
        
        Only reacts when a card is added
        """
        
        if len(addedcards) > 0:
        
            lector = self.read_card(readers())

            dni = lector[0]
            name = lector[1]

            self.logger.info(name + " has inserted the DNI " + dni)
    
            if(len(dni) != 0 and self.ldap.search(dni)):
                self.door_handler.open_door()
                self.logger.info("Access granted")
            else:
                self.logger.info("Access denied")
    
    def load_config(self, config_file_path):
        """
        Carga la configuracion del ldap, en la ruta que se le indica
        """
        return yaml.load(file(config_file_path, 'r'))
    
    
    def read_card(self, reader):
        """
        Read the data from the reader given as a parameters
        It actually takes an array of readers, but only access the first one
        """
        # Debug
        # I know, I should use a proper logger
        # r=readers()
        # print r
        
        if len(reader) > 0: 
        
            connection = reader[0].createConnection()
            connection.connect()
    
            # I'm not really sure how this works, legacy
            SELECT = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x50, 0x15]
            data, sw1, sw2 = connection.transmit( SELECT )
            #print "%x %x" % (sw1, sw2)
            SELECT = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x60, 0x04]
            data, sw1, sw2 = connection.transmit( SELECT )
            #print "%x %x" % (sw1, sw2)
            SELECT = [0x00, 0xC0, 0x00, 0x00, 0x1C]
            data, sw1, sw2 = connection.transmit( SELECT )
            #print "%x %x" % (sw1, sw2)
            SELECT = [0x00, 0xB0, 0x00, 0x00, 0xFF]
            data, sw1, sw2 = connection.transmit( SELECT )
            #print "%x %x" % (sw1, sw2)
            
            # In 'data' there are a lot of characters and random crap.
            # I use regexp to get the relevant pieces.
            
            ascii_data = toASCIIString(data)
    
            dni_regexp = re.search('(\d{8})[A-Z]', ascii_data)
            #TODO: make sure there actually are results
            dni = dni_regexp.group(1)
    
            # So, this is a little hellish. The names can be single or compound,
            # one or two surnames, again single or complex...
            # i.e:
            # John Doe Dui
            # Jane Maria Doe Dui
            # Johnny Doe Dui-Dao <-- Luckyly, the '-' is stored as a blank in the dni-e
            # Jenny Dolores Doe del Dui
            #
            
            name_regexp = re.search('\w*\s?\w*\s?\w*\s?\w+\s\w+,\s\w+\s\w*\s?\(AUTENTICACIÓN\)', ascii_data)
            
            # The name would look like:
            # DOE EOD, JOHN (AUTENTICACIÓN)
            
            name_raw = name_regexp.group().replace(" (AUTENTICACIÓN)", "")
            name_array = name_raw.split(", ")
            name = "%s %s" % (name_array[1], name_array[0])
    
            return dni, name
    
        else:
            print "Cannot found any reader. Is it connected?"
            sys.exit()
