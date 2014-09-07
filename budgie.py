#! /bin/env python

# budgie.py - pythonic remote control of servers via ssh
#  by Dale Stirling (@puredistortion) and Darren Wurf (@dwurf)
# Module loading code from sh.py, by Andrew Moffat (used under MIT license)

from types import ModuleType
import sys
import sh
import functools

__version__ = "0.01"

##### Exceptions #####
class SSHConfigError(Exception): pass
class SSHError(Exception): pass
class SSHObjCreate(Exception): pass



##### Module Class/Methods #####

class ssh(sh.Command):
    # TODO: Fix obscure errors when server is unknown
    # TODO: Detect and report when ssh keys aren't in place
    # TODO: ssh-agent support
    # TODO: Arbitrary config file
    # TODO: Detect and report when server fingerprint is unknown

    def __init__(self, host=None):  
        self._host = host
        ssh_cmd = super(ssh, self).__init__('ssh')

        # If a host is supplied then we add the host into the sh.Command class
        # instance at class initiation.
        if host:
            # Manually bake the host into the ssh command
            self._partial = True
            self._partial_baked_args.append(host)
            return ssh_cmd
        else:
            # Return generic ssh command instance
            return ssh_cmd

    def __call__(self, *args, **kwargs):
        if len(self._partial_baked_args) > 1:
            if args:
                return super(ssh, self).__call__(args, kwargs)
            else:
                return super(ssh, self).__call__(kwargs)
        raise NotImplementedError('''Call command eg. cadre.host.cmd(param)''')

    # reimplemented bake to enable hostgroups
    def bake(self, *args, **kwargs):
        fn = ssh()
        fn._host = self._host
        fn._partial = True

        call_args, kwargs = self._extract_call_args(kwargs)

        pruned_call_args = call_args
        for k, v in ssh._call_args.items():
            try:
                if pruned_call_args[k] == v:
                    del pruned_call_args[k]
            except KeyError: continue

        fn._partial_call_args.update(self._partial_call_args)
        fn._partial_call_args.update(pruned_call_args)
        fn._partial_baked_args.extend(self._partial_baked_args)
        sep = pruned_call_args.get("long_sep", self._call_args["long_sep"])
        fn._partial_baked_args.extend(self._compile_args(args, kwargs, sep))
        return fn


        
class HostGroup(dict):
    def __init__(self, hosts=[]):
        super(HostGroup, self).__init__()
        self.add(hosts)

    def __call__(self, *args, **kwargs):
       raise NotImplementedError('''Call command eg. budgie.HostGroup.cmd(param)''')

    def __getattr__(self, command):
        return functools.partial(self.run, command)

    def __build_host(self, host):
        if isinstance(host, ssh):
            return host._host, host
        elif isinstance(host, str):
            return host, ssh(host)
        else:
            raise SSHObjCreate('Host supplied to HostGroup could not be added')

    def run(self, command, *args, **kwargs):
        result_dict = {}
        for host in self:
            result_dict[host] = getattr(self[host], command)(*args, **kwargs)
        return result_dict

    def add(self, hosts):
        host_dict = {}
        if isinstance(hosts, list):
            for host in hosts:
                host_name, ssh_obj = self.__build_host(host)
                host_dict[host_name] = ssh_obj
        else:
            host_name, ssh_obj = self.__build_host(hosts)
            host_dict[host_name] = ssh_obj
        self.update(host_dict)

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
        for attr in ["__builtins__", "__doc__", "__name__", "__package__", "ssh", "HostGroup"]:
            setattr(self, attr, getattr(self_module, attr, None))

        # python 3.2 (2.7 and 3.3 work fine) breaks on osx (not ubuntu)
        # if we set this to None.  and 3.3 needs a value for __path__
        self.__path__ = []
        self.self_module = self_module

    def __getattr__(self, name):    
        # Here we bake the defined ssh host to the ssh() command
        return ssh(name)

# Setup default ssh_hosts.
# This ignores the exception and creates an empty ssh_config list as the 
# location of the ssh config file may need to be updated using set_ssh_config()

# And away we go 
self = sys.modules[__name__]
sys.modules[__name__] = SelfWrapper(self)
