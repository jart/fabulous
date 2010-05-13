
from __future__ import with_statement

import time
import curses


class Canvas(object):
    def __init__(self, encoding='UTF-8'):
        self.encoding = encoding

    def __enter__(self):
        self.win = curses.initscr()
        curses.start_color()
        curses.init_color(200, 1000, 300, 0)
        curses.init_pair(1, 200, curses.COLOR_WHITE)
        return self

    def __exit__(self, type_, value, traceback):
        curses.endwin()

    def __setitem__(self, xy, val):
        self.win.attron(curses.color_pair(1))
        (x, y) = xy
        self.win.addch(x, y, val)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')
    encoding = locale.getpreferredencoding()
    with Canvas(encoding=encoding) as canvas:
        canvas[5, 5] = 'Y'
        canvas.win.refresh()
        time.sleep(5.0)
