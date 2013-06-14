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
  of the connection you want to use. These are python-ldap, pyyaml and pyscard
  
  In a Debian based system, you can easily install them through aptitude_:
        
      aptitude install python-ldap python-yaml python-pyscard python-dev

  Also, depending on wich port you want to use, you will want to install different
  libraries:
  
#### Parallel port
     
  The pyparallel library is needed, avaliable through the python-parallel package
  in Debian:
  
    aptitude install python-parallel
           
#### Serial port
  
  In this case, you will need pyserial. In Debian:
  
    aptitude install python-pyserial
  
#### Raspberry pi GPIO
     
  You need to install the rpi.gpio avaliable at https://pypi.python.org/pypi/RPi.GPIO
  To install it, download the package and run:
  
    tar zxf RPi.GPIO-0.5.2a.tar.gz
    cd RPi.GPIO-0.5.2a
    sudo python setup.py install
    
  Remember to change '0.5.2a' for the version number corresponding to the one you
  download.
  
  Alternatively, you can install the version avaliable through the raspberry 
  repositories, python-rpi.gpio.
  
    aptitude install python-rpi.gpio
  
         
### Configuration

  Once you have decided wich port to use, you need to generate and edit the 
  configuration file:
    
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
Copyright (c) 2013, Alberto Mardomingo

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
  - Neither the name of the organization nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

