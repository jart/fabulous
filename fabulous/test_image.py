
import time

from fabulous.image import *


def test_balls():
    rep = []

    t = time.time()
    s = str(Image('balls.png'))
    print s
    print "rendered in %.4f sec using %d bytes (print method)" % (
        time.time() - t, len(s))

    t = time.time()
    for line in Image('balls.png'):
        print line
    print "rendered in %.4f sec (iter method)" % (time.time() - t)

    for s in rep:
        print s


class DebugImage(Image):
    def reduce(self, colors):
        need_reset = False
        line = ''
        for color, items in itertools.groupby(colors):
            if color is None:
                if need_reset:
                    line = line[:-1] + ">"
                    need_reset = False
                line += 'T' + ('  ' * len(list(items)))[1:]
            elif color == "EOL":
                if need_reset:
                    line = line[:-1] + ">"
                    need_reset = False
                    yield line.rstrip(' T')
                else:
                    yield line.rstrip(' T')
                line = ''
            else:
                need_reset = True
                line += '<' + ('  ' * len(list(items)))[1:]


def test_jellyfish():
    """I've never been creeped out by a unit test until now

    Maximize terminal and set font size small.
    """
    for line in DebugImage('balls.png'):
        print line


if __name__ == '__main__':
    test_balls()
    test_jellyfish()
