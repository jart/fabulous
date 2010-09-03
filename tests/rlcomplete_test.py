#!/usr/bin/env python

import unittest
from terminate import rlcomplete

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
