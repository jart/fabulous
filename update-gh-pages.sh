#!/bin/bash
#
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
