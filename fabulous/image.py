
import sys
from PIL import Image
from fabulous.ansi import fg


def image(path, resize=None):
    im = Image.open(path)
    if resize:
        im = im.resize(resize, Image.ANTIALIAS)
    pix = im.load()
    (width, height) = im.size
    for y in xrange(height):
        for x in xrange(width):
            sys.stdout.write(unicode(fg(pix[x, y], u"\u2588")).encode('utf8'))
        sys.stdout.write("\n")
