"""
    fabulous.image
    ~~~~~~~~~~~~~~

"""

import sys
import itertools

import grapefruit as gf

from fabulous import utils, xterm256


class Image(object):
    """Printing image files to a terminal

    I use :mod:`PIL` to turn your image file into a bitmap, resize it
    so it'll fit inside your terminal, and implement methods so I can
    behave like a string or iterable.

    When resizing, I'll assume that a single character on the terminal
    display is one pixel wide and two pixels tall.  For most fonts
    this is the best way to preserve the aspect ratio of your image.

    All colors are are quantized by :mod:`fabulous.xterm256` to the
    256 colors supported by modern terminals.  When quantizing
    semi-transparant pixels (common in text or PNG files) I'll ask
    :class:`TerminalInfo` for the background color I should use to
    solidify the color.  Fully transparent pixels will be rendered as
    a blank space without color so we don't need to mix in a
    background color.

    I also put a lot of work into optimizing the output line-by-line
    so it needs as few ANSI escape sequences as possible.  You can use
    :class:`DebugImage` to visualize these optimizations.
    """

    pad = ' '

    def __init__(self, path, width=None):
        utils.pil_check()
        from PIL import Image as PillsPillsPills
        self.img = PillsPillsPills.open(path)
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
                    color = gf.Color.NewFromRgb(*[c / 255.0 for c in rgba])
                    rgba = gf.Color.AlphaBlend(color, utils.term.bgcolor).rgb
                    yield xterm256.rgb_to_xterm(
                        *[int(c * 255.0) for c in rgba])
            yield "EOL"


def main(args):
    """I provide a command-line interface for this module
    """
    for imgpath in args[1:]:
        for line in Image(imgpath):
            print line


if __name__ == '__main__':
    main(sys.argv)
