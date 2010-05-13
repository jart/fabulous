"""
    fabulous.logs
    ~~~~~~~~~~~~~

    I provide utilities for making your logs look fabulous.

"""

import sys
import logging

from fabulous import utils


class TransientStreamHandler(logging.StreamHandler):
    """Standard Python logging Handler for Transient Console Logging

    Logging transiently means that verbose logging messages like DEBUG
    will only appear on the last line of your terminal for a short
    period of time and important messages like WARNING will scroll
    like normal text.

    This allows you to log lots of messages without the important
    stuff getting drowned out.

    This module integrates with the standard Python logging module.
    """

    def __init__(self, strm=sys.stderr, level=logging.WARNING):
        logging.StreamHandler.__init__(self, strm)
        if isinstance(level, int):
            self.levelno = level
        else:
            self.levelno = logging._levelNames[level]
        self.need_cr = False
        self.last = ""
        self.parent = logging.StreamHandler

    def close(self):
        if self.need_cr:
            self.stream.write("\n")
            self.need_cr = False
        self.parent.close(self)

    def write(self, data):
        if self.need_cr:
            width = max(min(utils.term.width, len(self.last)), len(data))
            fmt = "\r%-" + str(width) + "s\n" + self.last
        else:
            fmt = "%s\n"
        try:
            self.stream.write(fmt % (data))
        except UnicodeError:
            self.stream.write(fmt % (data.encode("UTF-8")))

    def transient_write(self, data):
        if self.need_cr:
            self.stream.write('\r')
        else:
            self.need_cr = True
        width = utils.term.width
        for line in data.rstrip().split('\n'):
            if line:
                if len(line) > width:
                    line = line[:width - 3] + '...'
                line_width = max(min(width, len(self.last)), len(line))
                fmt = "%-" + str(line_width) + "s"
                self.last = line
                try:
                    self.stream.write(fmt % (line))
                except UnicodeError:
                    self.stream.write(fmt % (line.encode("UTF-8")))
            else:
                self.stream.write('\r')
                self.stream.flush()

    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelno >= self.levelno:
                self.write(msg)
            else:
                self.transient_write(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def basicConfig(level=logging.WARNING, transient_level=logging.NOTSET):
    """Shortcut for setting up transient logging

    I am a replica of ``logging.basicConfig`` which installs a
    transient logging handler to stderr.
    """
    fmt = "%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s"
    logging.root.setLevel(transient_level)  # <--- IMPORTANT
    hand = TransientStreamHandler(level=level)
    hand.setFormatter(logging.Formatter(fmt))
    logging.root.addHandler(hand)
