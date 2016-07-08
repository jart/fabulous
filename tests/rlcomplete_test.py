#!/usr/bin/env python
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

import unittest
from fabulous import rlcomplete

class TestControl(unittest.TestCase):

    def test_ListCompleter(self):
        c = rlcomplete.ListCompleter(['foo','bar','baz'], True)
        self.failUnlessEqual(c.completelist('a'), [])
        self.failUnlessEqual(c.completelist('B'), ['bar','baz'])
        self.failUnlessEqual(c.completelist('f'), ['foo'])
        c = rlcomplete.ListCompleter(['foo','bar','baz'], False)
        self.failUnlessEqual(c.completelist('B'), [])
        self.failUnlessEqual(c.completelist('b'), ['bar','baz'])

    def test_PathCompleter(self):
        #c = rlcomplete.PathCompleter()
        #self.failUnlessEqual(c.completelist('m'), ['manual/'])
        pass
        
if __name__ == '__main__':
    unittest.main()

#Desktop/    bin/  lib/    personal/  src/  workspace/
#Templates/  doc/  media/  share/     tmp/  www/
