
import sys

from PIL import Image

# from fabulous.ansi import fg
from fabulous.test_xterm256 import fg


def image(path, resize=None, resize_antialias=None):
    im = Image.open(path)
    if resize:
        im = im.resize(resize)
    elif resize_antialias:
        im = im.resize(resize, Image.ANTIALIAS)
    pix = im.load()
    (width, height) = im.size
    for y in xrange(height):
        for x in xrange(width):
            color = pix[x, y]
            if len(color) == 4 and color[3] <= 0.001:
                s = sys.stdout.write(' ')
            else:
                sys.stdout.write(unicode(fg(color, u"\u2588")).encode('utf8'))
        sys.stdout.write("\n")



if __name__ == '__main__':
    print image('balls.png', resize=(100, 37))
