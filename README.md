cadre
=====

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
        


