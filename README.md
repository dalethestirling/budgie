cadre
=====

[![Build Status](https://travis-ci.org/puredistortion/cadre.png?branch=master)](https://travis-ci.org/puredistortion/cadre)

A pythonic remote control of servers via ssh

Installation
------------

Install the library

        virtualenv venv && . venv/bin/activate  # optional
        pip install sh
        wget https://raw2.github.com/dwurf/cadre/master/cadre.py


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

        from cadre import localhost
        print localhost.hostname(), localhost.uptime()
        localhost.touch('/tmp/latest')

You can also callhosts ing this alternate method if the magic above is to much

        import cadre
        print cadre.ssh('localhost'), cadre.ssh('localhost').uptime()
        cadre.ssh('localhost').touch('/tmp/latest')


Passing in SSH Options
----------------------
Cadre will allow the passing in of SSH options. Ath this time this is done through the bake method in the same way you would pass this into the sh.ssh()

        cadre.localhost.bake('-o', 'UserKnownHostsFile=/dev/null', '-o',  'StrictHostKeyChecking=no').whoami()

or 

        cadre.ssh().bake('-o', 'UserKnownHostsFile=/dev/null', '-o',  'StrictHostKeyChecking=no', '127.0.0.1').whoami()

This does need to be cleaned up to make more logical sense.  

Running Tests
-------------

`tests.py` can be called via the commandlime and is run on each commit through Travis CI

Tests can be called by running

        python tests.py

This is the current test suite being applied to builds
    *Import Test
    *Direct Call Goes to Exception Test
    *Command Execution (whoami) Test

Command execution test uses SSH options that allow for the automatic generation of SSH keypairs and discarding them from known hosts at the conclusion of the connection.



