#!/usr/bin/env python

import unittest
from terminate import casts

class TestControl(unittest.TestCase):

    def test_casts_yes_no(self):
        self.failUnlessEqual(casts.yes_no('y'), True)
        self.failUnlessEqual(casts.yes_no('n'), False)
        self.failUnlessEqual(casts.yes_no('Yes'), True)
        self.failUnlessEqual(casts.yes_no('nO'), False)
        self.failUnlessRaises(ValueError, casts.yes_no, 'spam')
        
    def test_casts_file(self):
        self.failUnlessEqual( type(casts.file(__file__)), type(open(__file__)) )
        self.failUnlessRaises(ValueError, casts.file, '')
        

if __name__ == '__main__':
    unittest.main()