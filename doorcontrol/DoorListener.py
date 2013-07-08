#!/usr/bin/python -tt
# -*- coding: UTF-8 -*-

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), 'door'))
#sys.path.append(os.path.join(os.path.dirname(__file__), 'serial'))
#sys.path.append(os.path.join(os.path.dirname(__file__), './raspberry'))

import string
import time
import logging
import yaml

import AuthConnector

from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.util import toASCIIString
from smartcard.CardMonitoring import CardMonitor, CardObserver

# flag that always appears before the dnie
DNI_SEPARATOR = "55 04 05 13"

# flag that always appears before the name
NAME_SEPARATOR = "55 04 03 0C"

class DoorListener( CardObserver ):

    def __init__ (self,auth_connector, config_path, logger):
        """
        Initializes the door_listener
        As parameters, it needs the auth connector, the path to the config
        file with the parameters for the port, and a logger
        """

        self.auth = auth_connector
        self.config = self.load_config(config_path)
        self.logger = logger

        
        #Select the card port
        if (self.config['parallel']['use']):
            import door.parallel as Door
            self.door_handler = Door.Door(self.config['parallel'], self.logger)
        elif (self.config['serial']['use']):
            import door.ser as Door
            self.door_handler = Door.Door(self.config['serial'], self.logger)
        elif (self.config['raspberry']['use']):
            import door.raspberry as Door
            self.door_handler = Door.Door(self.config['raspberry'], self.logger)
        else:
            self.logger.error("cannot recognize configuration")
            sys.exit()
        

    # Method to be added to the observer
    def update(self, observable, (addedcards, removedcards)):
        """
        Method called when a card is inserted or removed from the card reader
        
        Only reacts when a card is added
        """
        
        if len(addedcards) > 0:

            lector = self.read_card(addedcards[0])
            
            dni = lector[0]
            name = lector[1]
            
            self.logger.info(name + " has inserted the DNI " + dni)
            
            if self.auth.search(dni):
                self.door_handler.open_door()
                self.logger.info("Access granted")
            else:
                self.logger.info("Access denied")
    
    def load_config(self, config_file_path):
        """
        Carga la configuracion, en la ruta que se le indica
        """
        return yaml.load(file(config_file_path, 'r'))
    
    
    def read_card(self, card):
        """
        Read the data from the reader given as a parameters
        It actually takes an array of readers, but only access the first one
        """
        # Debug
        # I know, I should use a proper logger
        # r=readers()
        # print r
        
        if card is not None: 
        
            connection = card.createConnection()
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
            
            # In 'data' there are a lot of data and "flags" or fixed values.
            # I'll use those flags to select the dni and the name
            
            # So, first, i'll convert the data to its hex values:
            hex_data = toHexString(data)
            
            # For the dni, I get the data AFTER the flag,
            # and delete the first empty char:
            dnie_data = hex_data.split(DNI_SEPARATOR)[1].split(" ")[1:]
            
            # So, here, the first value is the dnie length, and then comes the dni
            dnie = dnie_data[1:(int(dnie_data[0], 16))]
            
            # If I were to get the letter:
            #dnie = dnie_data[1:(int(dnie_data[0], 16)+1)]
            
            # Note: int(val, 16) interprets the char as base 16 (i.e, as hexadecimal)
            # instead of as a decimal value (base 10)
            
            # Finally, I convert the values to ascii
            dni = "".join([chr(int(num, 16)) for num in dnie])
            
            
            # Now, for the name, is pretty much the same, just with a different flag
            name_data = hex_data.split(NAME_SEPARATOR)[1].split(" ")[1:]

            # The hex values for the name
            name_values = name_data[1:(int(name_data[0], 16)+0x01)]
            # Remeber, the first value in name_data is the length, so
            # I don't select it!
            
            # Convert the values to ascii
            name_list =  [chr(int(c, 16)) for c in name_values]
            
            # So, now, in name_unordered I have something like 
            # SURNAME1 SURNAME2, NAME (AUTENTICACIÓN)
            # So I'll process it a little bit to get it in the format
            # NAME SURNAME1 SURNAME2
            name_unordered =  "".join(name_list).replace("(AUTENTICACIÓN)", "")
            
            # Another option would have been reduce the length by 34 in name_values
            # to get rid of the "(AUTENTICACIÓN)" part, but I don't really like
            # magic numbers. So I use a magic string instead ;-P
            
            # Finally, the sorted name
            name = name_unordered.split(", ")[1] + name_unordered.split(", ")[0]

            return dni, name
    
        else:
            print "Cannot found any reader. Is it connected?"
            sys.exit()
