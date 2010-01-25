"""Print Images to a 256-Color Terminal
"""

import sys
import fcntl
import struct
import termios
import itertools

from PIL import Image as Pills
from grapefruit import Color

from fabulous.xterm256 import rgb_to_xterm


class Image(object):
    def __init__(self, path, width=None, bgcolor='black'):
        self.bgcolor = Color.NewFromHtml(bgcolor)
        self.img = Pills.open(path)
        self.resize(width)

    def __str__(self):
        return "\n".join(self)

    def __iter__(self):
        return self.reduce(self.convert())

    def resize(self, width=None):
        (iw, ih) = self.img.size
        if width is None:
            width = _term_width()
            if iw * 2 <= width:
                return
        width //= 2
        height = int(float(ih) * (float(width) / float(iw)))
        self.img = self.img.resize((width, height))

    def reduce(self, colors):
        need_reset = False
        line = []
        for color, items in itertools.groupby(colors):
            if color is None:
                if need_reset:
                    line.append("\x1b[49m")
                    need_reset = False
                line.append('  ' * len(list(items)))
            elif color == "EOL":
                if need_reset:
                    line.append("\x1b[49m")
                    need_reset = False
                    yield "".join(line)
                else:
                    line.pop()
                    yield "".join(line)
                line = []
            else:
                need_reset = True
                line.append("\x1b[48;5;%dm%s" % (color, '  ' * len(list(items))))

    def convert(self):
        (width, height) = self.img.size
        pix = self.img.load()
        for y in xrange(height):
            for x in xrange(width):
                rgba = pix[x, y]
                if len(rgba) == 4 and rgba[3] == 0:
                    yield None
                elif len(rgba) == 3 or rgba[3] == 255:
                    yield rgb_to_xterm(rgba[:3])
                else:
                    color = Color.NewFromRgb(*[c / 255.0 for c in rgba])
                    yield rgb_to_xterm(color.AlphaBlend(self.bgcolor))
            yield "EOL"


def _term_width():
    call = fcntl.ioctl(0, termios.TIOCGWINSZ, "\000" * 8)
    height, width = struct.unpack("hhhh", call)[:2]
    return width
