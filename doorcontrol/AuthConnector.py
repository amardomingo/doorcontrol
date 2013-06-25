# -*- coding: UTF-8 -*-

import yaml

import logging


class LdapConnector:

    def __init__ (self,config, logger):
        """
        Initializes the ldap connector, with the config file path
        and a logger passed as parameters
        """
        self.config = self.load_config(config)
        
         #Select the card port
        if (self.config['file']['use']):
            import auth.file as AuthConnector
            self.auth_connector = AuthConnector.AuthConnector(self.config['file'], self.logger)
        elif (self.config['ldap']['use']):
            import auth.ldap as  Door
            self.auth_connector = AuthConnector.AuthConnector(self.config['ldap'], self.logger)
        else:
            logger.error("cannot recognize auth configuration")
            sys.exit()


    def load_config(self,config):
        """
        Carga la configuracion del ldap, en la ruta que se le indica
        """
        file_config = file(config, 'r')
        
        ldap_config = yaml.load(file_config)
        
        return ldap_config

    def search(self,dni):
        return self.auth_connector.search(dni)
	    
        except Exception as e:
            #print e
            self.logger.error(e)
            # handle error however you like
