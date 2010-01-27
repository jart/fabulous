"""Print Images to a 256-Color Terminal
"""

import sys
import itertools

from PIL import Image as Pills
from grapefruit import Color

from fabulous import utils, xterm256


class Image(object):
    pad = ' '

    def __init__(self, path, width=None, bgcolor='white'):
        self.img = Pills.open(path)
        self.bgcolor = Color.NewFromHtml(bgcolor)
        self.resize(width)

    def __str__(self):
        return "\n".join(self)

    def __iter__(self):
        # strip out blank lines
        for line in self.reduce(self.convert()):
            if line.strip():
                yield line
        yield ""

    @property
    def size(self):
        return self.img.size

    def resize(self, width=None):
        (iw, ih) = self.size
        if width is None:
            width = min(iw, utils.term.width)
        elif isinstance(width, basestring):
            percents = dict([(pct, '%s%%' % (pct)) for pct in range(101)])
            width = percents[width]
        height = int(float(ih) * (float(width) / float(iw)))
        height //= 2
        self.img = self.img.resize((width, height))

    def reduce(self, colors):
        need_reset = False
        line = []
        for color, items in itertools.groupby(colors):
            if color is None:
                if need_reset:
                    line.append("\x1b[49m")
                    need_reset = False
                line.append(self.pad * len(list(items)))
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
                line.append("\x1b[48;5;%dm%s" % (
                    color, self.pad * len(list(items))))

    def convert(self):
        (width, height) = self.img.size
        pix = self.img.load()
        for y in xrange(height):
            for x in xrange(width):
                rgba = pix[x, y]
                if len(rgba) == 4 and rgba[3] == 0:
                    yield None
                elif len(rgba) == 3 or rgba[3] == 255:
                    yield xterm256.rgb_to_xterm(*rgba[:3])
                else:
                    color = Color.NewFromRgb(*[c / 255.0 for c in rgba])
                    rgba = color.AlphaBlend(self.bgcolor).rgb
                    yield xterm256.rgb_to_xterm(*[int(c * 255.0) for c in rgba])
            yield "EOL"


if __name__ == '__main__':
    for imgpath in sys.argv[1:]:
        for line in Image(imgpath):
            print line
