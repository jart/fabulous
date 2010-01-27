
from ez_setup import use_setuptools
use_setuptools(version='0.6c9')

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name                 = 'fabulous',
    version              = __import__('fabulous').__version__,
    author               = 'J.A. Roberts Tunney',
    author_email         = 'jtunney@lobstertech.com',
    description          = 'Makes your terminal output totally fabulous',
    download_url         = 'https://bitbucket.org/jart/fabulous/get/tip.tar.gz',
    long_description     = read('README'),
    license              = 'BSD',
    install_requires     = ['grapefruit'],
    packages             = find_packages(),
    setup_requires       = ["setuptools_hg"],
    zip_safe             = False,
    # http://wiki.python.org/moin/CheeseShopTutorial
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Artistic Software",
        "Topic :: System :: Logging",
        "Topic :: Multimedia :: Graphics"
        "Topic :: Terminals :: Terminal Emulators/X Terminals",
    ],
)
