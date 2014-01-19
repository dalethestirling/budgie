#! /bin/env python

# cadre.py - pythonic remote control of servers via ssh
# Module loading code from sh.py, by Andrew Moffat (used under MIT license)

from types import ModuleType
import os.path 
import sys
import re 
import sh

##### Set defaults #####
global __ssh_config__
__ssh_config__ = os.path.expanduser("~/.ssh/config")

##### Exceptions #####

class SSHConfigError(Exception): pass


##### Helpers #####
def _get_config_hosts(ssh_config):
    '''Collects the configured hosts from ssh config file'''
    # Regex to collect Host definitions from ssh config
    host_regex = re.compile('^Host( |=| = )([A-Za-z0-9-_]+)$')

    # Here the file is validated and Host names are extracted from teh ssh config
    if not os.path.isfile(ssh_config):
        raise SSHConfigError("SSH Config file %s is not found" % ssh_config)
    with file(ssh_config) as ssh_read:
        host_array = [host_regex.match(line).group(2) for line in ssh_read if host_regex.match(line)]

    return host_array

def _is_config_host(ssh_host):
    '''Checks that host exists in the ssh config of the current user'''
   
    if not ssh_host in __ssh_hosts__:
        raise SSHConfigError('HOST %s not defined in %s' % (ssh_host, __ssh_config__))


##### Module Class/Methids #####
def set_ssh_config(new_ssh_config):
    '''Updates the zsh_config path and gets hosts from config'''        
    try:
        global __ssh_hosts__
        __ssh_hosts__ = _get_config_hosts(new_ssh_config)
    except SSHConfigError as e:
        raise e
    else:
        global __ssh_config__
        __ssh_config__ = new_ssh_config


class ssh(sh.Command):
    # TODO
    # Disallow ssh.__call__()
    # Fix obscure errors when server is unknown
    # Detect and report when ssh keys aren't in place
    # ssh-agent support
    # Arbitrary config file
    # Detect and report when server fingerprint is unknown
    def __init__(self):
        return super(ssh, self).__init__('ssh')


# this is a thin wrapper around THIS module (we patch sys.modules[__name__]).
# this is in the case that the user does a "from bomdiggity import whatever"
# in other words, they only want to import certain programs, not the whole
# system PATH worth of commands.  in this case, we just proxy the
# import lookup to our Environment class
class SelfWrapper(ModuleType):
    def __init__(self, self_module):
        # this is super ugly to have to copy attributes like this,
        # but it seems to be the only way to make reload() behave
        # nicely.  if i make these attributes dynamic lookups in
        # __getattr__, reload sometimes chokes in weird ways...
        for attr in ["__builtins__", "__doc__", "__name__", "__package__", "set_ssh_config", "_is_config_host", "_get_config_hosts"]:
            setattr(self, attr, getattr(self_module, attr, None))

        # python 3.2 (2.7 and 3.3 work fine) breaks on osx (not ubuntu)
        # if we set this to None.  and 3.3 needs a value for __path__
        self.__path__ = []
        self.self_module = self_module

    def __getattr__(self, name):
        # First we validate if the host had been defined in the specified ssh conf
        # If not defined a SSHConfigError exception is raised.
        _is_config_host(name)

        # Here we bake the defined ssh host to the ssh() command
        return ssh().bake(name)

# Setup default ssh_hosts.
# This ignores the exception and creates an empty ssh_config list as the 
# location of the ssh config file may need to be updated using set_ssh_config()
global __ssh_hosts__
try:
    __ssh_hosts__ = _get_config_hosts(__ssh_config__)
except SSHConfigError:
    __ssh_hosts__ = []

# And away we go 
self = sys.modules[__name__]
sys.modules[__name__] = SelfWrapper(self)