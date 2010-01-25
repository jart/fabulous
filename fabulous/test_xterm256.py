# -*- coding: utf-8 -*-

import sys

from fabulous.xterm256 import *


esc = lambda code: u"\x1b[%sm" % (code)
bold = lambda s: esc(1) + s + esc(22)
fg = lambda color, s: esc("38;5;%d" % (rgb_to_xterm(color))) + s + esc(39)
bg = lambda color, s: esc("48;5;%d" % (rgb_to_xterm(color))) + s + esc(49)


def test_hello():
    s = 'hello old ' + bold('ANSI BOLD')
    print "%s (Raw: %r)" % (s, s)
    # assert s == 'hello old \x1b[1mANSI BOLD\x1b[22m'

    s = 'hello new ' + bold(bg('#FAB82A', fg('#525252', 'XTERM-256')))
    print "%s (Raw: %r)" % (s, s)
    # assert s == ('hello new \x1b[1m\x1b[48;5;214m\x1b[38;5;239m'
    #              'XTERM-256\x1b[39m\x1b[49m\x1b[22m')


def test_rainbow():
    word = 'XTERMINAL256'
    rainbow = ['#f00', '#f90', '#ff0', '#090', '#00f', '#c09']
    s = ''
    for color, char1, char2 in zip(rainbow, word[::2], word[1::2]):
        s += bg(color, "".join(char1 + char2))
    s = fg('#000', s)
    print "rainbow: %s (Raw: %r)" % (s, s)
    # assert s == ('\x1b[38;5;0m\x1b[48;5;9mXT'
    #              '\x1b[49m\x1b[48;5;208mER'
    #              '\x1b[49m\x1b[48;5;11mMI'
    #              '\x1b[49m\x1b[48;5;28mNA'
    #              '\x1b[49m\x1b[48;5;21mL2'
    #              '\x1b[49m\x1b[48;5;162m56'
    #              '\x1b[49m\x1b[39m')


def test_box():
    """What a miserable failure
    """
    corn = u"◢◣◥◤" # u"◤◥◣◢"
    bord = '#ff0000'
    fill = '#00ff00'
    box = [fg(bord, corn[0]) + bg(bord, ' ' * 10) + fg(bord, corn[1]),
           bg(bord, ' ')     + bg(fill, ' ' * 10) + bg(bord, ' '),
           fg(bord, corn[2]) + bg(bord, ' ' * 10) + fg(bord, corn[3])]
    print "\n".join(box).encode('UTF-8')


def test_grayscale():
    from grapefruit import Color
    for n in xrange(0, 256, 15):
        sys.stdout.write(bg((n, n, n), '  '))
    print " Grayscale"


def test_alpha_grayscale(bgcolor):
    from grapefruit import Color
    bgc = Color.NewFromHtml(bgcolor, 1.0)
    for n in xrange(0, 256, 5):
        fgc = Color.NewFromRgb(1, 1, 1, n / 255.0)
        c = fgc.AlphaBlend(bgc)
        sys.stdout.write(bg(c, ' '))
    print " Alpha Grayscale (%s background)" % (bgcolor)


def test_cubes():
    print "\nHappy Cubes:"
    cube_color = lambda x,y,z: 16 + x + y*6 + z*6*6
    for y in range(6):
        for z in range(6):
            for x in range(6):
                xc = cube_color(x, y, z)
                sys.stdout.write(esc("48;5;%d" % (xc)) + '  ' + esc(49))
            sys.stdout.write(" ")
        sys.stdout.write("\n")


if __name__ == '__main__':
    test_hello()
    test_rainbow()
    test_grayscale()
    test_alpha_grayscale('black')
    test_alpha_grayscale('red')
    test_alpha_grayscale('green')
    test_alpha_grayscale('blue')
    test_cubes()
