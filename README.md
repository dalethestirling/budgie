budgie
======

[![Build Status](https://travis-ci.org/puredistortion/cadre.png?branch=master)](https://travis-ci.org/puredistortion/cadre)
[![Build Status](https://travis-ci.org/puredistortion/budgie.png?branch=master)](https://travis-ci.org/puredistortion/budgie)

A pythonic remote control of servers via ssh

Installation
------------

Install the library

        virtualenv venv && . venv/bin/activate  # optional
        pip install sh
        wget https://raw2.github.com/puredistortion/budgie/master/budgie.py


You need to configure passwordless SSH for your remote hosts:

        ssh-keygen -q -t rsa -N 'your_password_here' -f ~/.ssh/id_rsa
        ssh-copy-id localhost # Repeat this for each host
        eval `ssh-agent`
        ssh-add
        ssh localhost pwd # test connection

Next, create an SSH config file in `~/.ssh/config` describing your hosts:

        Host localhost
            User user
            HostName localhost
            IdentityFile ~/.ssh/id_rsa.key

        Host osx
            User user
            HostName steve-mac
            IdentityFile ~/.ssh/id_rsa.key

        Host projects
            User user
            HostName 192.168.1.30
            IdentityFile ~/.ssh/projects.key

        Host prod
            User produser
            HostName prod.example.com
            IdentityFile ~/.ssh/deploy.key

Usage
-----

Now you can run remote commands using simple python code

        from budgie import localhost
        print localhost.hostname(), localhost.uptime()
        localhost.touch('/tmp/latest')

You can also callhosts ing this alternate method if the magic above is to much

        import budgie
        print budgie.ssh('localhost'), budgie.ssh('localhost').uptime()
        budgie.ssh('localhost').touch('/tmp/latest')


Passing in SSH Options
----------------------
budgie will allow the passing in of SSH options. At this time this is done through the bake method in the same way you would pass this into the sh.ssh()

        budgie.localhost.bake('-o', 'UserKnownHostsFile=/dev/null', '-o',  'StrictHostKeyChecking=no').whoami()

or 

        budgie.ssh().bake('-o', 'UserKnownHostsFile=/dev/null', '-o',  'StrictHostKeyChecking=no', '127.0.0.1').whoami()

This does need to be cleaned up to make more logical sense.  

Budgie Host Groups
-----------------
budgie offers the ability to bundle ssh hosts for batch command execution. This is done through creating a host group. A host group will take in a list of host names or budgie.ssh instances.

        web_servers = budgie.HostGroup()
        web_servers.add('www1.example.com')
        web_servers.add('www2.example.com')

        webservers.add(['www1.example.com', 'www2.example.com'])

        www1 = budgie.ssh('www1.example.com')
        www2 = budgie.ssh('www2.example.com')
        webservers.add([www1, www2])

or

        web_servers.HostGroup(['www1.example.com', 'www2.example.com'])

        www1 = budgie.ssh('www1.example.com')
        www2 = budgie.ssh('www2.example.com')
        web_servers.HostGroup([www1, www2])

Once a budgie.HostGroup() is created it can be intereacted with like a standard dictionary.

Commands can be executed against the host group and results of execution will be supplied back as a dictionary

        result = web_servers.whoami()

Result would contain

        {'www1': 'www1.example.com', 'www2': 'www2.example.com'}



Running Tests
-------------

`tests.py` can be called via the commandlime and is run on each commit through Travis CIq

Tests can be called by running

        python tests.py

This is the current test suite being applied to builds
    *Import Test
    *Direct Call Goes to Exception Test
    *Command Execution (whoami) Test
    *HostGroup Creation
    *HostGroup Manipulation (add, remove)
    *HostGroup Command Execution (whoami) Test

Command execution test uses SSH options that allow for the automatic generation of SSH keypairs and discarding them from known hosts at the conclusion of the connection.



