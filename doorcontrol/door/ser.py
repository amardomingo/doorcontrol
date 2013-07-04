# -*- coding: UTF-8 -*-

import sys

import serial
import string
import re


class Door:
  
    def __init__ (self,config, logger):
        """
        Initializes the door
        
        It takes the door config and a logger as parameters,
        """
        self.config = config
        self.logger = logger
    
    def open_door(self):
        """
        Opens the door
        """

        # The serial port to open
        port = int(self.config['port'])

        # I send a ramdom text, and use the "data ready" pin.
        text = "Clava Thessara Infinitas"
        # "Key to infinite treasure", in Alteran (Ancient)
        
        # Try an open the serial port
        try:
            # Create the port
            serialport = serial.Serial(port, 75)
            serialport.timeout=1;
            
            # Send the text so the pin is set to 1
            serialport.write(text)
            
            # Close the port. Should probably be in the "finally"
            serialport.close()
        except Exception as e:
            self.logger.error("Cannot open the serial port")
            self.logger.error(e)
