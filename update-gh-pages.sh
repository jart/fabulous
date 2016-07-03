#!/bin/bash
git diff --shortstat | grep -q . && { echo repo is dirty; exit 1; }
set -ex
sudo python setup.py install
sudo chown -R jart .
git clean -fdx
rm -rf gh-pages
sphinx-build docs /tmp/fabulous-gh-pages
git checkout gh-pages
cp -R /tmp/fabulous-gh-pages/* .
cp -R /tmp/fabulous-gh-pages/.doctrees .
cp /tmp/fabulous-gh-pages/.buildinfo .
git add .
git commit -m 'Rebuild Sphinx documentation'
git push origin gh-pages
git checkout master
rm -rf /tmp/fabulous-gh-pages
