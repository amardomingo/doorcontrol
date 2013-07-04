# -*- coding: UTF-8 -*-

import yaml

import logging


class AuthConnector:

    def __init__ (self,config, logger):
        """
        Initializes the ldap connector, with the config file path
        and a logger passed as parameters
        """
        self.config = self.load_config(config)
        self.logger = logger
        
         #Select the card port
        if (self.config['file']['use']):
            import auth.file as FileConnector
            self.auth_connector = FileConnector.AuthConnector(self.config['file'], self.logger)
        elif (self.config['ldap']['use']):
            import auth.ldapconnect as  LdapConnector
            self.auth_connector = LdapConnector.AuthConnector(self.config['ldap'], self.logger)
        else:
            self.logger.error("cannot recognize auth configuration")
            sys.exit()


    def load_config(self,config):
        """
        Carga la configuracion del ldap, en la ruta que se le indica
        """
        file_config = file(config, 'r')
        
        ldap_config = yaml.load(file_config)
        
        return ldap_config

    def search(self,dni):
        try:
            return self.auth_connector.search(dni)
	    
        except Exception as e:
            self.logger.error("Error searching the dni")
            self.logger.error(e)
