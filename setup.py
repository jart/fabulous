# Copyright 2016 The Fabulous Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# http://packages.python.org/distribute/setuptools.html
# http://diveintopython3.org/packaging.html
# http://wiki.python.org/moin/CheeseShopTutorial
# http://pypi.python.org/pypi?:action=list_classifiers

import os

try:
    import setuptools
except ImportError:
    import ez_setup
    ez_setup.use_setuptools(version='0.6c11')
    import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = __import__('fabulous').__version__

setuptools.setup(
    name                 = 'fabulous',
    version              = version,
    url                  = 'https://jart.github.io/fabulous',
    author               = 'Justine Tunney',
    author_email         = 'jtunney@gmail.com',
    description          = 'Makes your terminal output totally fabulous',
    download_url         = ('https://github.com/jart/fabulous/releases'
                            '/download/' + version +
                            '/fabulous-' + version + '.tar.gz'),
    long_description     = read('README.rst'),
    license              = 'Apache 2.0 / OFL',
    packages             = ['fabulous', 'fabulous.experimental'],
    zip_safe             = False,
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'fabulous-demo = fabulous.demo:main',
            'fabulous-gotham = fabulous.gotham:main',
            'fabulous-image = fabulous.image:main',
            'fabulous-rotatingcube = fabulous.rotating_cube:main',
            'fabulous-text = fabulous.text:main',
        ],
    },
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Artistic Software",
        "Topic :: System :: Logging",
        "Topic :: Multimedia :: Graphics"
    ],
)
