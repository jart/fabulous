#!/usr/bin/env python

"""Outputs something like:
spaand eggs
george
"""

from terminate.term import stdout

stdout.write('spam')
stdout.move('left')
stdout.write('and')
stdout.move('right')
stdout.write('eggs')
stdout.move('left',3)
stdout.move('down')
stdout.write('george')
print # trailing newline
