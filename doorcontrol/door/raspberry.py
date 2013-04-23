# -*- coding: UTF-8 -*-

import sys
import serial
import string
import re

import RPi.GPIO as GPIO

from time import sleep


class Door:
  
  def __init__ (self,config, logger):
    """
    Initializes the door

    It takes the door config and a logger as parameters,
    
    Be advised: only give the config corresponding to the port, not 
    the full config
    """
    self.config = config
    self.logger = logger


  def open_door(self):
    """
    Opens the door using the gpio port
    """
    
    # The gpio pin to use
    pin = int(self.config["pin"])
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    # Try and use the gpio
    try:
        # Sets the port to true, and wait a bit
        GPIO.output(pin, 1)
        sleep(5)
        
        # Close the door!
        GPIO.output(pin, 0)
        
    except serial.SerialException:
        self.logger.error("Cannot open the gpio")
        self.logger.error(e)
        
    # Clean everything
    GPIO.cleanup()
