
from fabulous.xterm256 import *


esc = lambda code: u"\x1b[%sm" % (code)
bold = lambda s: esc(1) + s + esc(22)
fg = lambda color, s: esc("38;5;%d" % (rgb_to_xterm(color))) + s + esc(39)
bg = lambda color, s: esc("48;5;%d" % (rgb_to_xterm(color))) + s + esc(49)


def test_hello():
    s = 'hello old ' + bold('ANSI BOLD')
    print "%s (Raw: %r)" % (s, s)
    assert s == 'hello old \x1b[1mANSI BOLD\x1b[22m'

    s = 'hello new ' + bold(bg('#FAB82A', fg('#525252', 'XTERM-256')))
    print "%s (Raw: %r)" % (s, s)
    assert s == ('hello new \x1b[1m\x1b[48;5;214m\x1b[38;5;239m'
                 'XTERM-256\x1b[39m\x1b[49m\x1b[22m')


def test_rainbow():
    word = 'XTERMINAL256'
    rainbow = ['#f00', '#f90', '#ff0', '#090', '#00f', '#c09']
    s = ''
    for color, char1, char2 in zip(rainbow, word[::2], word[1::2]):
        s += bg(color, "".join(char1 + char2))
    s = fg('#000', s)
    print "rainbow: %s (Raw: %r)" % (s, s)
    assert s == ('\x1b[38;5;0m\x1b[48;5;9mXT'
                 '\x1b[49m\x1b[48;5;208mER'
                 '\x1b[49m\x1b[48;5;11mMI'
                 '\x1b[49m\x1b[48;5;28mNA'
                 '\x1b[49m\x1b[48;5;21mL2'
                 '\x1b[49m\x1b[48;5;162m56'
                 '\x1b[49m\x1b[39m')


if __name__ == '__main__':
    test_hello()
    test_rainbow()
