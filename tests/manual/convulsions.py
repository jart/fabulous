#!/usr/bin/env python

"""I am *not* responsible if this causes severe physical or mental injury
"""

from terminate.term import display, stdout, Magic
        

try:
    while True:
        for c in Magic.COLORS.iterkeys():
            stdout.write(display(bg=c))
            stdout.move('down',4)
except KeyboardInterrupt:
    stdout.write(display('default'))
    print
    print "Interupt from keyboard. Exiting."