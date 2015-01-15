#!/usr/bin/env python

from setuptools import setup

setup(name='budgie',
      version='0.1',
      description='Pythonic remote commands via ssh',
      author='Dale Stirling and Darren Wurf',
      author_email='feedback@puredistortion.com',
      url='http://www.python.org/puredistortion/budgie',
      py_modules=['budgie'],
      install_requires=['sh'],
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
     )