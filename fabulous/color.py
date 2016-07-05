# -*- coding: utf-8 -*-
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

"""
    fabulous.color
    ~~~~~~~~~~~~~~

    The color module provides an object-oriented abstraction for stylized text
    inside the terminal. This includes things like bold text, blinking text,
    4-bit ANSI colors and 8-bit xterm256 colors.

"""

import sys
import functools

from fabulous import utils, xterm256, grapefruit


OVERLINE = u'\u203e'


def esc(*codes):
    """Produces an ANSI escape code string from a list of integers

    This is a low level function that is abstracted by the other functions and
    classes in this module.

    """
    return "\x1b[%sm" % (";".join([str(c) for c in codes]))


class ColorString(object):
    r"""Abstract base class for stylized string-like objects.

    Subclasses make it possible to compose stylized text::

        >>> str(red("hello"))
        '\x1b[31mhello\x1b[39m'
        >>> str(bold(red("hello")))
        '\x1b[1m\x1b[31mhello\x1b[39m\x1b[22m'
        >>> str(plain("hello ", bold("world")))
        'hello \x1b[1mworld\x1b[22m'

    These objects also provide string length without taking into consideration
    the ANSI escape codes::

        >>> len(red("hello"))
        5
        >>> len(str(red("hello")))
        15
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
    r"""Base class for 256-color stylized string-like objects.

    See the :class:`.fg256`, :class:`.bg256`, :class:`.highlight256`, and
    :class:`.complement256` classes for more information.

    """
    def __init__(self, color, *items):
        (r, g, b) = parse_color(color)
        self.color = xterm256.rgb_to_xterm(r, g, b)
        self.items = items

    def __str__(self):
        return self.fmt % (
            self.color, self.sep.join([unicode(s) for s in self.items]))


class plain(ColorString):
    r"""Plain text wrapper

    This class is useful for concatenating plain strings with
    :class:`.ColorString` objects. For example::

        from fabulous.color import plain
        >>> len(plain("hello ", bold("kitty")))
        11

    """
    pass


class bold(ColorString):
    r"""Bold text wrapper

    This class creates a string-like object containing bold or bright text. It
    also brightens the foreground and background colors. This is supported by
    all terminals that support ANSI color codes.

    Example usage::

        from fabulous.color import bold
        print bold('i am bold!')
        print plain('hello ', bold('world'))

    The ANSI escape codes are as follows::

        >>> str(bold("hello"))
        '\x1b[1mhello\x1b[22m'

    """
    fmt = esc(1) + "%s" + esc(22)


class italic(ColorString):
    r"""Italic text wrapper

    This class creates a string-like object containing italic text, which is
    supported by almost no terminals.

    The ANSI escape codes are as follows::

        >>> str(italic("hello"))
        '\x1b[3mhello\x1b[23m'

    """
    fmt = esc(3) + "%s" + esc(23)


class underline(ColorString):
    r"""Underline text wrapper

    This class creates a string-like object containing underline text. This is
    supported by SOME terminals, as documented in the terminal support section.

    Example usage::

        from fabulous.color import underline
        print underline('i am underlined!')
        print plain('hello ', underline('world'))

    The ANSI escape codes are as follows::

        >>> str(underline("hello"))
        '\x1b[4mhello\x1b[24m'

    """
    fmt = esc(4) + "%s" + esc(24)


class underline2(ColorString):
    r"""Alternative underline text wrapper

    See also: :class:`.underline`.

    The ANSI escape codes are as follows::

        >>> str(underline2("hello"))
        '\x1b[21mhello\x1b[24m'

    """
    fmt = esc(21) + "%s" + esc(24)


class strike(ColorString):
    r"""Strike-through text wrapper

    This class creates a string-like object containing strike-through text,
    which is supported by very few terminals.

    Example usage::

        from fabulous.color import strike
        print strike('i am stricken!')
        print plain('hello ', strike('world'))

    The ANSI escape codes are as follows::

        >>> str(strike("hello"))
        '\x1b[9mhello\x1b[29m'

    """
    fmt = esc(9) + "%s" + esc(29)


class blink(ColorString):
    r"""Blinking text wrapper

    This class creates a string-like object containing blinking text. This is
    supported by SOME terminals, as documented in the terminal support section.

    Example usage::

        from fabulous.color import blink
        print blink('i am underlined!')
        print plain('hello ', blink('world'))

    The ANSI escape codes are as follows::

        >>> str(blink("hello"))
        '\x1b[5mhello\x1b[25m'

    """
    fmt = esc(5) + "%s" + esc(25)


class flip(ColorString):
    r"""Flips background and foreground colors

    For example::

        from fabulous.color import flip, red
        print flip(red('hello'))

    Is equivalent to the following on a black terminal::

        from fabulous.color import black, red_bg
        print red_bg(black('hello'))

    The ANSI escape codes are as follows::

        >>> str(flip("hello"))
        '\x1b[7mhello\x1b[27m'

    """
    fmt = esc(7) + "%s" + esc(27)


class black(ColorString):
    r"""Black foreground text wrapper

    This class creates a string-like object containing text with a black
    foreground.

    Example usage::

        from fabulous.color import black
        print black('i am black!')
        print plain('hello ', black('world'))

    Text can be made dark grey by using :class:`.bold`::

        from fabulous.color import bold, black
        print bold(black('i am dark grey!'))

    The ANSI escape codes are as follows::

        >>> str(black("hello"))
        '\x1b[30mhello\x1b[39m'

    """
    fmt = esc(30) + "%s" + esc(39)

class red(ColorString):
    r"""Red foreground text wrapper

    This class creates a string-like object containing text with a red
    foreground.

    Example usage::

        from fabulous.color import red
        print red('i am red!')
        print plain('hello ', red('world'))

    Text can be made bright red by using :class:`.bold`::

        from fabulous.color import bold, red
        print bold(red('i am bright red!'))

    The ANSI escape codes are as follows::

        >>> str(red("hello"))
        '\x1b[31mhello\x1b[39m'

    """
    fmt = esc(31) + "%s" + esc(39)


class green(ColorString):
    r"""Green foreground text wrapper

    This class creates a string-like object containing text with a green
    foreground.

    Example usage::

        from fabulous.color import green
        print green('i am green!')
        print plain('hello ', green('world'))

    Text can be made bright green by using :class:`.bold`::

        from fabulous.color import bold, green
        print bold(green('i am bright green!'))

    The ANSI escape codes are as follows::

        >>> str(green("hello"))
        '\x1b[32mhello\x1b[39m'

    """
    fmt = esc(32) + "%s" + esc(39)


class yellow(ColorString):
    r"""Yellow foreground text wrapper

    This class creates a string-like object containing text with a "yellow"
    foreground, which in many terminals is actually going to look more
    brownish.

    Example usage::

        from fabulous.color import yellow
        print yellow('i am yellow brownish!')
        print plain('hello ', yellow('world'))

    Text can be made true bright yellow by using :class:`.bold`::

        from fabulous.color import bold, yellow
        print bold(yellow('i am bright yellow!'))

    The ANSI escape codes are as follows::

        >>> str(yellow("hello"))
        '\x1b[33mhello\x1b[39m'

    """
    fmt = esc(33) + "%s" + esc(39)


class blue(ColorString):
    r"""Blue foreground text wrapper

    This class creates a string-like object containing text with a blue
    foreground.

    Example usage::

        from fabulous.color import blue
        print blue('i am dark blue!')
        print plain('hello ', blue('world'))

    Text can be made sky blue by using :class:`.bold`::

        from fabulous.color import bold, blue
        print bold(blue('i am sky blue!'))

    The ANSI escape codes are as follows::

        >>> str(blue("hello"))
        '\x1b[34mhello\x1b[39m'

    """
    fmt = esc(34) + "%s" + esc(39)


class magenta(ColorString):
    r"""Purple/magenta foreground text wrapper

    This class creates a string-like object containing text with a magenta
    foreground. Although in many terminals, it's going to look more purple.

    Example usage::

        from fabulous.color import magenta
        print magenta('i am magenta purplish!')
        print plain('hello ', magenta('world'))

    Text can be made hot pink by using :class:`.bold`::

        from fabulous.color import bold, magenta
        print bold(magenta('i am hot pink!'))

    The ANSI escape codes are as follows::

        >>> str(magenta("hello"))
        '\x1b[35mhello\x1b[39m'

    """
    fmt = esc(35) + "%s" + esc(39)


class cyan(ColorString):
    r"""Cyan foreground text wrapper

    This class creates a string-like object containing text with a cyan
    foreground.

    Example usage::

        from fabulous.color import cyan
        print cyan('i am cyan!')
        print plain('hello ', cyan('world'))

    Text can be made bright cyan by using :class:`.bold`::

        from fabulous.color import bold, cyan
        print bold(cyan('i am bright cyan!'))

    The ANSI escape codes are as follows::

        >>> str(cyan("hello"))
        '\x1b[36mhello\x1b[39m'

    """
    fmt = esc(36) + "%s" + esc(39)


class white(ColorString):
    r"""White foreground text wrapper

    This class creates a string-like object containing text with a light grey
    foreground.

    Example usage::

        from fabulous.color import white
        print white('i am light grey!')
        print plain('hello ', white('world'))

    Text can be made true white by using :class:`.bold`::

        from fabulous.color import bold, white
        print bold(white('i am bold white!'))

    The ANSI escape codes are as follows::

        >>> str(white("hello"))
        '\x1b[37mhello\x1b[39m'

    """
    fmt = esc(37) + "%s" + esc(39)


class highlight_black(ColorString):
    r"""Dark grey highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.black`.

    """
    fmt = esc(1, 30, 7) + "%s" + esc(22, 27, 39)


class highlight_red(ColorString):
    r"""Red highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.red`.

    """
    fmt = esc(1, 31, 7) + "%s" + esc(22, 27, 39)


class highlight_green(ColorString):
    r"""Green highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.green`.

    """
    fmt = esc(1, 32, 7) + "%s" + esc(22, 27, 39)


class highlight_yellow(ColorString):
    r"""Yellow highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.yellow`.

    """
    fmt = esc(1, 33, 7) + "%s" + esc(22, 27, 39)


class highlight_blue(ColorString):
    r"""Blue highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.blue`.

    """
    fmt = esc(1, 34, 7) + "%s" + esc(22, 27, 39)


class highlight_magenta(ColorString):
    r"""Hot pink highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.magenta`.

    """
    fmt = esc(1, 35, 7) + "%s" + esc(22, 27, 39)


class highlight_cyan(ColorString):
    r"""Cyan highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.cyan`.

    """
    fmt = esc(1, 36, 7) + "%s" + esc(22, 27, 39)


class highlight_white(ColorString):
    r"""White highlight text wrapper

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.yellow`.

    """
    fmt = esc(1, 37, 7) + "%s" + esc(22, 27, 39)


class black_bg(ColorString):
    r"""Black background text wrapper

    This class creates a string-like object containing text with a black
    background. On properly configured terminals, this will do nothing.

    Example usage::

        from fabulous.color import black_bg
        print black_bg('i have a black background!')
        print plain('hello ', black_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(black_bg("hello"))
        '\x1b[40mhello\x1b[49m'

    """
    fmt = esc(40) + "%s" + esc(49)


class red_bg(ColorString):
    r"""Red background text wrapper

    This class creates a string-like object containing text with a red
    background.

    Example usage::

        from fabulous.color import red_bg
        print red_bg('i have a red background!')
        print plain('hello ', red_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(red_bg("hello"))
        '\x1b[41mhello\x1b[49m'

    """
    fmt = esc(41) + "%s" + esc(49)


class green_bg(ColorString):
    r"""Green background text wrapper

    This class creates a string-like object containing text with a green
    background.

    Example usage::

        from fabulous.color import green_bg
        print green_bg('i have a green background!')
        print plain('hello ', green_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(green_bg("hello"))
        '\x1b[42mhello\x1b[49m'

    """
    fmt = esc(42) + "%s" + esc(49)


class yellow_bg(ColorString):
    r"""Yellow background text wrapper

    This class creates a string-like object containing text with a yellow
    background.

    Example usage::

        from fabulous.color import yellow_bg
        print yellow_bg('i have a yellow background!')
        print plain('hello ', yellow_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(yellow_bg("hello"))
        '\x1b[43mhello\x1b[49m'

    """
    fmt = esc(43) + "%s" + esc(49)


class blue_bg(ColorString):
    r"""Blue background text wrapper

    This class creates a string-like object containing text with a blue
    background.

    Example usage::

        from fabulous.color import blue_bg
        print blue_bg('i have a blue background!')
        print plain('hello ', blue_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(blue_bg("hello"))
        '\x1b[44mhello\x1b[49m'

    """
    fmt = esc(44) + "%s" + esc(49)


class magenta_bg(ColorString):
    r"""Magenta background text wrapper

    This class creates a string-like object containing text with a magenta
    background.

    Example usage::

        from fabulous.color import magenta_bg
        print magenta_bg('i have a magenta background!')
        print plain('hello ', magenta_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(magenta_bg("hello"))
        '\x1b[45mhello\x1b[49m'

    """
    fmt = esc(45) + "%s" + esc(49)


class cyan_bg(ColorString):
    r"""Cyan background text wrapper

    This class creates a string-like object containing text with a cyan
    background.

    Example usage::

        from fabulous.color import cyan_bg
        print cyan_bg('i have a cyan background!')
        print plain('hello ', cyan_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(cyan_bg("hello"))
        '\x1b[46mhello\x1b[49m'

    """
    fmt = esc(46) + "%s" + esc(49)


class white_bg(ColorString):
    r"""White background text wrapper

    This class creates a string-like object containing text with a white
    background.

    Example usage::

        from fabulous.color import white_bg
        print white_bg('i have a white background!')
        print plain('hello ', white_bg('world'))

    The ANSI escape codes are as follows::

        >>> str(white_bg("hello"))
        '\x1b[47mhello\x1b[49m'

    """
    fmt = esc(47) + "%s" + esc(49)


class fg256(ColorString256):
    r"""xterm256 foreground color wrapper

    This class creates a string-like object that has an xterm256 color. The
    color is specified as a CSS color code, which is automatically quantized to
    the available set of xterm colors.

    These colors are more dependable than the 4-bit colors, because 8-bit
    colors don't get changed by the terminal theme. They will consistently be
    the requested color, which is calculated using a simple math formula.

    However it is worth noting that in Terminal.app on Mac OS, 8-bit colors
    appear to be designed rather than formulaic, so they look much nicer.

    Example usage::

        from fabulous import fg256, plain
        print fg256('#F00', 'i am red!')
        print fg256('#FF0000', 'i am red!')
        print fg256('magenta', 'i am', ' magenta!')
        print plain('hello ', fg256('magenta', 'world'))

    The ANSI escape codes look as follows::

        >>> str(fg256('red', 'hello'))
        '\x1b[38;5;196mhello\x1b[39m'

    """
    fmt = esc(38, 5, "%d") + "%s" + esc(39)


class bg256(ColorString256):
    r"""xterm256 background color wrapper

    This class creates a string-like object that has an xterm256 color. The
    color is specified as a CSS color code, which is automatically quantized to
    the available set of xterm colors.

    These colors are more dependable than the 4-bit colors, because 8-bit
    colors don't get changed by the terminal theme. They will consistently be
    the requested color.

    However it is worth noting that in Terminal.app on Mac OS, 8-bit background
    colors are ever so slightly different than their foreground equivalent.
    Therefore Terminal.app has effectively 512 colors.

    Example usage::

        from fabulous import bg256, plain
        print bg256('#F00', 'i have a red background!')
        print bg256('#FF0000', 'i have a red background!')
        print bg256('magenta', 'i have a', ' magenta background!')
        print plain('hello ', bg256('magenta', 'world'))

    The ANSI escape codes look as follows::

        >>> str(bg256('red', 'hello'))
        '\x1b[48;5;196mhello\x1b[49m'

    """
    fmt = esc(48, 5, "%d") + "%s" + esc(49)


class highlight256(ColorString256):
    r"""Highlighted 8-bit color text

    This is equivalent to composing :class:`.bold`, :class:`.flip`, and
    :class:`.fg256`.

    """
    fmt = esc(1, 38, 5, "%d", 7) + "%s" + esc(27, 39, 22)


class complement256(ColorString256):
    r"""Highlighted 8-bit color text

    This class composes :class:`.bold`, :class:`.flip`, and
    :class:`.bg256`. Then it invokes :meth:`complement` to supply the polar
    opposite :class:`fg256` color.

    This looks kind of hideous at the moment. We're planning on finding a
    better formula for complementary colors in the future.

    """
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
    """Prints bold text with line beneath it spanning width of terminal
    """
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
    r"""Calculates polar opposite of color

    This isn't guaranteed to look good >_> (especially with brighter, higher
    intensity colors.) This will be replaced with a formula that produces
    better looking colors in the future.

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
