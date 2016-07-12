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

from fabulous.term import display, Magic, Term
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
        for color in Magic.COLORS.keys():
            self.set_display(fg=color)
            stdout.write("    " + color)
        
        self.set_display('default')
        
        stdout.write("regular background test:")
        for color in Magic.COLORS.keys():
            self.set_display(bg=color)
            stdout.write("    " + color)
        
        self.set_display('default')
        
        stdout.write("bright foreground test:")
        self.set_display('bright')
        for color in Magic.COLORS.keys():
            self.set_display(fg=color)
            stdout.write("    " + color)
        
        self.set_display('default')
        
        stdout.write("dim foreground test:")
        self.set_display('dim')
        for color in Magic.COLORS.keys():
            self.set_display(fg=color)
            stdout.write("    " + color)
        
        self.set_display('bright','red')
        stdout.write("bright red")
        self.set_display("default")

if __name__ == '__main__':
    unittest.main()
