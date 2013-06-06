"""
    fabulous.utils
    ~~~~~~~~~~~~~~

"""

import os
import sys
import fcntl
import struct
import termios
import textwrap
import functools

import grapefruit


def memoize(function):
    """A very simple memoize decorator to optimize pure-ish functions

    Don't use this unless you've examined the code and see the
    potential risks.
    """
    cache = {}
    @functools.wraps(function)
    def _memoize(*args):
        if args in cache:
            return cache[args]
        result = function(*args)
        cache[args] = result
        return result
    return function


class TerminalInfo(object):
    """Quick and easy access to some terminal information

    I'll tell you the terminal width/height and it's background color.

    You don't need to use me directly.  Just access the global
    :data:`term` instance::

        >>> assert term.width > 0
        >>> assert term.height > 0

    It's important to know the background color when rendering PNG
    images with semi-transparency.  Because there's no way to detect
    this, black will be the default::

        >>> term.bgcolor
        (0.0, 0.0, 0.0, 1.0)
        >>> import grapefruit
        >>> isinstance(term.bgcolor, grapefruit.Color)
        True

    If you use a white terminal, you'll need to manually change this::

        >>> term.bgcolor = 'white'
        >>> term.bgcolor
        (1.0, 1.0, 1.0, 1.0)
        >>> term.bgcolor = grapefruit.Color.NewFromRgb(0.0, 0.0, 0.0, 1.0)
        >>> term.bgcolor
        (0.0, 0.0, 0.0, 1.0)

    """

    def __init__(self, bgcolor='black'):
        self.bgcolor = bgcolor

    @property
    def termfd(self):
        """Returns file descriptor number of terminal

        This will look at all three standard i/o file descriptors and
        return whichever one is actually a TTY in case you're
        redirecting i/o through pipes.
        """
        for fd in (2, 1, 0):
            if os.isatty(fd):
                return fd
        raise Exception("No TTY could be found")

    @property
    def dimensions(self):
        """Returns terminal dimensions

        Don't save this information for long periods of time because
        the user might resize their terminal.

        :return: Returns ``(width, height)``.  If there's no terminal
                 to be found, we'll just return ``(79, 40)``.
        """
        try:
            call = fcntl.ioctl(self.termfd, termios.TIOCGWINSZ, "\000" * 8)
        except IOError:
            return (79, 40)
        else:
            height, width = struct.unpack("hhhh", call)[:2]
            return (width, height)

    @property
    def width(self):
        """Returns width of terminal in characters
        """
        return self.dimensions[0]

    @property
    def height(self):
        """Returns height of terminal in lines
        """
        return self.dimensions[1]

    def _get_bgcolor(self):
        return self._bgcolor

    def _set_bgcolor(self, color):
        if isinstance(color, grapefruit.Color):
            self._bgcolor = color
        else:
            self._bgcolor = grapefruit.Color.NewFromHtml(color)

    bgcolor = property(_get_bgcolor, _set_bgcolor)


term = TerminalInfo()


def pil_check():
    """Check for PIL library, printing friendly error if not found

    We need PIL for the :mod:`fabulous.text` and :mod:`fabulous.image`
    modules to work.  Because PIL can be very tricky to install, it's
    not listed in the ``setup.py`` requirements list.

    Not everyone is going to have PIL installed so it's best that we
    offer as much help as possible so they don't have to suffer like I
    have in the past :'(
    """
    try:
        import PIL
    except ImportError:
        raise ImportError(textwrap.dedent("""
            Oh no!  You don't have the evil PIL library!

            Here's how you get it:

            Ubuntu/Debian:

                sudo apt-get install python-imaging

            Mac OS X:

                http://pythonmac.org/packages/py24-fat/index.html
                http://pythonmac.org/packages/py25-fat/index.html

            Windows:

                http://effbot.org/downloads/PIL-1.1.7.win32-py%(pyversion)s.exe

            Everyone Else:

              This is like the hardest library in the world to
              manually install.  If your package manager doesn't have
              it, you can try running ``sudo easy_install pil`` once
              you get your hands on a C compiler as well as the
              following libraries (including the development headers)
              for Python, libz, libjpeg, libgif, libpng, libungif4,
              libfreetype6, and maybe more >_>

            """ % {'pyversion': "%s.%s" % sys.version_info[:2]}))
