#!/usr/bin/env python

from terminate.term import display, Magic, Term
import os
import unittest

devnull = open(os.devnull, 'w')
stdout = Term(devnull)

class TestTerm(unittest.TestCase):
    
    def set_display(self,codes=[], fg=None, bg=None):
        stdout.write(display(codes, fg, bg))

    def test_color(self):
        self.set_display('default')
        stdout.write("default text")
        
        stdout.write("regular foreground test:")
        for color in Magic.COLORS.iterkeys():
            self.set_display(fg=color)
            stdout.write("    " + color)
        
        self.set_display('default')
        
        stdout.write("regular background test:")
        for color in Magic.COLORS.iterkeys():
            self.set_display(bg=color)
            stdout.write("    " + color)
        
        self.set_display('default')
        
        stdout.write("bright foreground test:")
        self.set_display('bright')
        for color in Magic.COLORS.iterkeys():
            self.set_display(fg=color)
            stdout.write("    " + color)
        
        self.set_display('default')
        
        stdout.write("dim foreground test:")
        self.set_display('dim')
        for color in Magic.COLORS.iterkeys():
            self.set_display(fg=color)
            stdout.write("    " + color)
        
        self.set_display('bright','red')
        stdout.write("bright red")
        self.set_display("default")

if __name__ == '__main__':
    unittest.main()