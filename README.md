DoorControl
====================
Small phython utility to control a door using a smartcard reader

***WARNING: This is development level software.  Please do not use it unless you
             are familiar with what that means and are comfortable using that type
             of software. Also, be advised: it has not been tested yet, and the 
             parallel and serial options will probably never be. IT MAY NOT WORK
             AT ALL***


Installation & Configuration
----------------------------

### Dependencies:

  To run this utility, there are several python libraries required, independently
  of the connection you want to use. These are pyyaml and pyscard
  
  In a Debian based system, you can easily install them through aptitude:
        
      aptitude install python-yaml python-pyscard python-dev


#### Port dependencies:

  Also, depending on wich port you want to use, you will want to install different
  libraries:
  
##### Parallel port
     
  The pyparallel library is needed, available through the python-parallel package
  in Debian:
  
    aptitude install python-parallel
           
##### Serial port
  
  In this case, you will need pyserial. In Debian:
  
    aptitude install python-pyserial
  
##### Raspberry pi GPIO
     
  You need to install the rpi.gpio available at https://pypi.python.org/pypi/RPi.GPIO
  To install it, download the package and run:
  
    tar zxf RPi.GPIO-0.5.2a.tar.gz
    cd RPi.GPIO-0.5.2a
    sudo python setup.py install
    
  Remember to change '0.5.2a' for the version number corresponding to the one you
  download.
  
  Alternatively, you can install the version available through the raspberry 
  repositories, python-rpi.gpio.
  
    aptitude install python-rpi.gpio

#### Auth-system dependencies:
  
  You can use either ldap authentication, or a csv file with a list of names a DNIs
  on it. Each of them have different requirements:
  
##### LDAP Authentication

  In this case, you will need to install the python ldap module. In debian-like:
  
    aptitude install python-ldap
    
##### File Authentication

  The only needed module here is the python csv lib, which already comes with most
  of the python installations.
         
### Configuration

  Once you have decided wich port to use and the auth system, you need to generate
  and edit the configuration file:
    
    cd doorcontrol
    python mkconf.py

  If a conf.yml file already exists, it will ask you to overwrite it.
  
  Once you have a conf.yml in the doorcontrol/ folder, edit it and add both the
  port and ldap configuration.
  
### Run on startup

  If you want it run as a daemon, on startup, you should edit the bin/bootup file,
  and change the "DAEMON=/opt/doorcontrol/bin/$NAME" to point to the place you have
  downloaded it. Then, copy it to /etc/init.d/, rename it and register it:
    
    cp bin/bootup /etc/init.d/doorcontrol
    insserv doorcontrol
    update-rc.d doorcontrol defaults
  

Contributing
------------

There are several possible improvements that can be made, the most important one
beeing actually testing the parallel and serial options. Also, the code could be
clean up and, probably, there will be a better way of implementing most of it.

Feel free to do whatever you want, as long as you respect the license bellow.


About the Project
-----------------
DoorControl is a small utility based on the code of Pablo Moncada Isla to 
allow control of a door using an electronic lock and a smartcard reader, with
several improvements and modifications.

At the moment this document was written, parallel, serial and raspberry GPIO ports
are planned, although the serial and parallel only as a "proof of concept", as I 
don't have the resources nor the spare time to test them.


Contributors
----------------

* Alberto Mardomingo Mardomingo

* Pablo Moncada Isla


License
-------
DoorControl is a small python utilty to control a door with a card reader

Copyright (c) 2013, Alberto Mardomingo

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

