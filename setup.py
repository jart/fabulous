
from ez_setup import use_setuptools
use_setuptools(version='0.6c9')

import os
from setuptools import setup, find_packages

setup(
    name                 = 'fabulous',
    version              = __import__('fabulous').__version__,
    description          = 'Makes your terminal output totally fabulous',
    long_description     = open('README').read(),
    license              = 'WTFPL', # no licensing restrictions lol
    install_requires     = [],
    packages             = find_packages(),
    setup_requires       = ["setuptools_hg"],
    zip_safe             = True,
)
