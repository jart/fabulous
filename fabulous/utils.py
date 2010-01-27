
import fcntl
import struct
import termios

import grapefruit


class TerminalInfo(object):
    @property
    def dimensions(self):
        call = fcntl.ioctl(0, termios.TIOCGWINSZ, "\000" * 8)
        height, width = struct.unpack("hhhh", call)[:2]
        return width, height

    width = property(lambda self: self.dimensions[0])
    height = property(lambda self: self.dimensions[1])

    def _get_bgcolor(self):
        return self._bgcolor
    def _set_bgcolor(self, color):
        self._bgcolor = grapefruit.Color.NewFromHtml(color)
    bgcolor = property(_get_bgcolor, _set_bgcolor)


term = TerminalInfo()
term.bgcolor = 'black'


def pil_check():
    """Check for PIL with friendly error message

    We check for PIL at runtime because it'd be a far greater evil to
    put it in the setup_requires list.
    """
    try:
        import PIL
    except ImportError:
        raise ImportError(textwrap.dedent("""
            I'm sorry, I can't render images without PIL :'(

            Ubuntu Users: sudo apt-get install python-imaging

            Windows Users: The PIL people should have something easy to
              install that you can download from their website.

            Everyone Else: This is like the hardest library in the world
              to manually install.  If your package manager doesn't have
              it, you can try running ``sudo easy_install pil`` once you
              get your hands on a C compiler the development headers for
              ``python``, ``libz``, ``libjpeg``, ``libgif``, ``libpng``,
              ``libungif4``, ``libfreetype6``, and maybe more >_>
            """))
