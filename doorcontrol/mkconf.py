
import os.path
import readline


def write_config():
    conf = open('conf.yml', 'w')
    
    conf.write("# Config for the ldap \n\
ldap:\n\n\
    ## MANDATORY FIELDS ##\n\
    # The ldap server\n\
    server: localhost\n\n\
    # The search to authenticate\n\
    baseDN: ou=users,dc=example,dc=org\n\n\
    # The name the dni is stored in the ldap\n\
    dni_name: employeeNumber, sn\n\n\
    ## OPTIONAL FIELDS ##\n\
    # User and pass for the ldap\n\
    user: cn=admin,dc=example,dc=org\n\
    password: pass\n\n\
    # The ldap Version\n\
    version: 3\n\n\
# Config for the file\n\
file:\n\
    use: false\n\n\
    # URI, either local or url.\n\
    # The recomended structure is ['Name',DNI]\n\
    uri: uri/to/csv\n\n\
    # CSV data, optional\n\
    delimiter: ','\n\
    quotechar: '|'\n\
# Config options for the parallel port\n\
parallel:\n\n\
    use: false\n\n\
    # The pin number to open the door\n\
    pin: 1\n\n\
# Config options for the serial port\n\n\
serial:\n\n\
    use: false\n\n\
    port: 1\n\n\
    # No need to set pin number here, see the README for details\n\n\
# Config for the Raspberry GPIO port\n\
raspberry:\n\n\
    use: false\n\n\
    # The GPIO pin number to use\n\
    pin: 12\n")
    
    conf.close()


def main():
    if (os.path.exists('conf.yml')):
        override = raw_input('config file already exists. Overwrite? [y/N]:')
        override = override.strip()
        if (override.lower() != 'y'):
            return
    
    write_config()
    


if __name__ == '__main__':
    main();
