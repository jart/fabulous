#!/usr/bin/env python

from terminate.term import display, stdout, Magic

stdout.write(display('default'))
stdout.write("default text\n")

stdout.write("regular foreground test:\n")
for color in Magic.COLORS.iterkeys():
    stdout.write(display(fg=color))
    stdout.write("    " + color + '\n')

stdout.write(display('default'))

stdout.write("regular background test:\n")
for color in Magic.COLORS.iterkeys():
    stdout.write(display(bg=color))
    stdout.write("    " + color + '\n')

stdout.write(display('default'))

stdout.write("bright foreground test:\n")
stdout.write(display('bright'))
for color in Magic.COLORS.iterkeys():
    stdout.write(display(fg=color))
    stdout.write("    " + color + '\n')

stdout.write(display('default'))

stdout.write("dim foreground test:\n")
stdout.write(display('dim'))
for color in Magic.COLORS.iterkeys():
    stdout.write(display(fg=color))
    stdout.write("    " + color + '\n')

stdout.write(display('bright','red'))
stdout.write("bright red\n")
stdout.write(display("default"))
