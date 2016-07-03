# -*- coding: utf-8 -*-
"""
    fabulous.color
    ~~~~~~~~~~~~~~

    I implement support for standard 16-color color terminals.

"""

import sys
import functools

from fabulous import utils, xterm256, grapefruit


OVERLINE = u'\u203e'


def esc(*codes):
    return "\x1b[%sm" % (";".join([str(c) for c in codes]))


class ColorString(object):
    r"""A colorized string-like object that gives correct length

    If anyone knows a way to be able to make this behave like a string
    object without creating a bug minefield let me know::

        >>> str(red("hello"))
        '\x1b[31mhello\x1b[39m'
        >>> len(red("hello"))
        5
        >>> len(str(red("hello")))
        15
        >>> str(bold(red("hello")))
        '\x1b[1m\x1b[31mhello\x1b[39m\x1b[22m'
        >>> len(bold(red("hello")))
        5
        >>> len(bold("hello ", red("world")))
        11

    """
    sep = ""
    fmt = "%s"

    def __init__(self, *items):
        self.items = items

    def __str__(self):
        return self.fmt % (self.sep.join([unicode(s) for s in self.items]))

    def __repr__(self):
        return repr(unicode(self))

    def __len__(self):
        return sum([len(item) for item in self.items])

    def __add__(self, cs):
        if not isinstance(cs, (basestring, ColorString)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(cs), type(self)))
        return ColorString(self, cs)

    def __radd__(self, cs):
        if not isinstance(cs, (basestring, ColorString)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(self), type(cs)))
        return ColorString(cs, self)

    @property
    def as_utf8(self):
        """A more readable way to say ``unicode(color).encode('utf8')``
        """
        return unicode(self).encode('utf8')


class ColorString256(ColorString):
    def __init__(self, color, *items):
        (r, g, b) = parse_color(color)
        self.color = xterm256.rgb_to_xterm(r, g, b)
        self.items = items

    def __str__(self):
        return self.fmt % (
            self.color, self.sep.join([unicode(s) for s in self.items]))


class plain(ColorString):
    r"""A passive wrapper that preserves proper length reporting

    >>> len(plain("hello ", bold("kitty")))
    11
    """
    pass


class bold(ColorString):
    fmt = esc(1) + "%s" + esc(22)
class italic(ColorString):
    fmt = esc(3) + "%s" + esc(23)
class underline(ColorString):
    fmt = esc(4) + "%s" + esc(24)
class underline2(ColorString):
    fmt = esc(21) + "%s" + esc(24)
class strike(ColorString):
    fmt = esc(9) + "%s" + esc(29)
class blink(ColorString):
    fmt = esc(5) + "%s" + esc(25)
class flip(ColorString):
    fmt = esc(7) + "%s" + esc(27)


class black(ColorString):
    fmt = esc(30) + "%s" + esc(39)
class red(ColorString):
    fmt = esc(31) + "%s" + esc(39)
class green(ColorString):
    fmt = esc(32) + "%s" + esc(39)
class yellow(ColorString):
    fmt = esc(33) + "%s" + esc(39)
class blue(ColorString):
    fmt = esc(34) + "%s" + esc(39)
class magenta(ColorString):
    fmt = esc(35) + "%s" + esc(39)
class cyan(ColorString):
    fmt = esc(36) + "%s" + esc(39)
class white(ColorString):
    fmt = esc(37) + "%s" + esc(39)


class highlight_black(ColorString):
    fmt = esc(1, 30, 7) + "%s" + esc(22, 27, 39)
class highlight_red(ColorString):
    fmt = esc(1, 31, 7) + "%s" + esc(22, 27, 39)
class highlight_green(ColorString):
    fmt = esc(1, 32, 7) + "%s" + esc(22, 27, 39)
class highlight_yellow(ColorString):
    fmt = esc(1, 33, 7) + "%s" + esc(22, 27, 39)
class highlight_blue(ColorString):
    fmt = esc(1, 34, 7) + "%s" + esc(22, 27, 39)
class highlight_magenta(ColorString):
    fmt = esc(1, 35, 7) + "%s" + esc(22, 27, 39)
class highlight_cyan(ColorString):
    fmt = esc(1, 36, 7) + "%s" + esc(22, 27, 39)
class highlight_white(ColorString):
    fmt = esc(1, 37, 7) + "%s" + esc(22, 27, 39)


class black_bg(ColorString):
    fmt = esc(40) + "%s" + esc(49)
class red_bg(ColorString):
    fmt = esc(41) + "%s" + esc(49)
class green_bg(ColorString):
    fmt = esc(42) + "%s" + esc(49)
class yellow_bg(ColorString):
    fmt = esc(43) + "%s" + esc(49)
class blue_bg(ColorString):
    fmt = esc(44) + "%s" + esc(49)
class magenta_bg(ColorString):
    fmt = esc(45) + "%s" + esc(49)
class cyan_bg(ColorString):
    fmt = esc(46) + "%s" + esc(49)
class white_bg(ColorString):
    fmt = esc(47) + "%s" + esc(49)


class fg256(ColorString256):
    fmt = esc(38, 5, "%d") + "%s" + esc(39)


class bg256(ColorString256):
    fmt = esc(48, 5, "%d") + "%s" + esc(49)


class highlight256(ColorString256):
    fmt = esc(1, 38, 5, "%d", 7) + "%s" + esc(27, 39, 22)


class complement256(ColorString256):
    fmt = esc(1, 38, 5, "%d", 48, 5, "%d") + "%s" + esc(49, 39, 22)

    def __init__(self, color, *items):
        self.bg = xterm256.rgb_to_xterm(*parse_color(color))
        self.fg = xterm256.rgb_to_xterm(*complement(color))
        self.items = items

    def __str__(self):
        return self.fmt % (
            self.fg, self.bg,
            self.sep.join([unicode(s) for s in self.items]))


def h1(title, line=OVERLINE):
    width = utils.term.width
    print bold(title.center(width)).as_utf8
    print bold((line * width)[:width]).as_utf8


def parse_color(color):
    r"""Turns a color into an (r, g, b) tuple

    >>> parse_color('white')
    (255, 255, 255)
    >>> parse_color('#ff0000')
    (255, 0, 0)
    >>> parse_color('#f00')
    (255, 0, 0)
    >>> parse_color((255, 0, 0))
    (255, 0, 0)
    >>> from fabulous import grapefruit
    >>> parse_color(grapefruit.Color((0.0, 1.0, 0.0)))
    (0, 255, 0)
    """
    if isinstance(color, basestring):
        color = grapefruit.Color.NewFromHtml(color)
    if isinstance(color, int):
        (r, g, b) = xterm256.xterm_to_rgb(color)
    elif hasattr(color, 'rgb'):
        (r, g, b) = [int(c * 255.0) for c in color.rgb]
    else:
        (r, g, b) = color
    assert isinstance(r, int) and 0 <= r <= 255
    assert isinstance(g, int) and 0 <= g <= 255
    assert isinstance(b, int) and 0 <= b <= 255
    return (r, g, b)


def complement(color):
    r"""Gives you the polar opposite of your color

    This isn't guaranteed to look good >_> (especially with
    brighter, higher intensity colors.)

    >>> complement('red')
    (0, 255, 76)
    >>> complement((0, 100, 175))
    (175, 101, 0)
    """
    (r, g, b) = parse_color(color)
    gcolor = grapefruit.Color((r / 255.0, g / 255.0, b / 255.0))
    complement = gcolor.ComplementaryColor()
    (r, g, b) = [int(c * 255.0) for c in complement.rgb]
    return (r, g, b)


def section(title, bar=OVERLINE, strm=sys.stdout):
    """Helper function for testing demo routines
    """
    width = utils.term.width
    print >>strm, bold(title.center(width)).as_utf8
    print >>strm, bold((bar * width)[:width]).as_utf8
