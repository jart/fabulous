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
    download_url         = ('https://github.com/jart/fabulous/archive/' +
                            version + '.tar.gz'),
    long_description     = read('README.rst'),
    license              = 'MIT',
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
        "License :: OSI Approved :: MIT License",
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
