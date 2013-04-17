# -*- coding: UTF-8 -*-

import ldap
import yaml

import logger


class LdapConnector:

    def __init__ (self,config, logger):
        """
        Initializes the ldap connector, with the config file path
        and a logger passed as parameters
        """
        self.config = load_config(config)
        #By default, sets the ldap version to 3
        if not self.config.get('version'):
            self.config['version'] = 3
        self.logger = logger


    def load_config(config):
        """
        Carga la configuracion del ldap, en la ruta que se le indica
        """
        file_config = file(config, 'r')
        
        ldap_config = yaml.load(file_config).get('ldap')
        
        return ldap_config

    def search(dni):
        """
        Returns true if the given dni id found in the ldap
        """
        # Hint: devuelve un array de arrays de listas de hashes y no se que leches
        # (no necesariamente en ese orden)
        #
        # Para recuperar el nombre:
        # resu[0][0][1].get('cn')[0]
        #
        # Para el dni (sin letra):
        # resu[0][0][1].get('employeeNumber')[0]
        
        server = self.config['server']
        user = self.config['user']
        password = self.config['password']
        version = self.config['version']
        baseDN = self.config['baseDN']
        search_filter = self.config['dni_name']
    
        try:
            l = ldap.open(self.config['server'])
        
            # Si no conozco la version del ldap, utilizo 2 por defecto
            if (self.config['version'] == 3):
                l.protocol_version = ldap.VERSION3	
            else if (self.config['version'] == 2 ):
                l.protocol_version = ldap.VERSION2
            else:
                # I don't support this version of ldap.
                raise Exception('ldap version not supported')
                # To be fair, I'm not event sure this would work with ldap 2...
            
            # Utilizo el user y el pass que tengo
            # De no usarlos, tambien conseguiria acceso, con privilegios
            # limitados
            # Cualquier error lanza una excepcion ldap.LDAPError
            result_set = []
            l.simple_bind(self.config['user'],self.config['password'])
            for filt in  self.config['dni_name'].split(', '):
                ldap_result_id = l.search(elf.config['baseDN'], ldap.SCOPE_SUBTREE, filt + '=' + dni, None)
            
                result_type, result_data = l.result(ldap_result_id, 0)
                print result_type
                print result_data
            
                
                while result_data != []:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
                    result_type, result_data = l.result(ldap_result_id, 0)

            #Closing the connection to the ldap
            l.unbind()

            # I don't need to return the name nor the dni, I already knwe both!
            return result_set != []
	    
        except e:
            self.logger.error(e)
            # handle error however you like
