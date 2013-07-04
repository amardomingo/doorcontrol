# -*- coding: UTF-8 -*-

import sys
import parallel

import logging

from time import sleep

class Door:

    def __init__ (self,config, logger):
        """
        Initializes the door

        It takes the door config and a logger as parameters.

        Be advised: only give the config corresponding to the port, not 
        the full config
        """
        self.config = config
        self.logger = logger
    
    def open_door(self):
        """
        Opens the door
        No big deal, just opens it with the parallel port
        """
        # Abrir el puerto paralelo
        try:
            port = parallel.Parallel()
            
            # Depending on the number given to setData(.) it will turn a number
            # pins, translating the number passed as a parameter into binary.
            # 
            # D0   D1   D2   D3   D4   D5   D6   D7
            # 1    2    4    8    16   32   64   128
            #
            # For example, giving a '3' will turn on both D0 and D1, and giving 
            # '8' will only turn on de D3
            
            # This is hardware related!
            port.setData(int(self.config['pin']))

            # Make this a config option?
            sleep(5)
            
            # Apagando....
            port.setData(0)
        except e:
            #-- Error al abrir el puerto paralelo
            logger.error("Error al abrir puerto (%s)\n")
            sys.exit(e)
            #-- Lo vuelvo a intentar?
            # abrePuerta()



## TODO: Is a main needed?
def main(argv):
    open_door()

if __name__ == "__main__":
    main(sys.argv)
