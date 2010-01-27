
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

    bgcolor = grapefruit.Color.NewFromHtml('black')


term = TerminalInfo()
