
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
        return self.bgcolor
    def _set_bgcolor(self, color):
        self._bgcolor = grapefruit.Color.NewFromHtml(color)
    bgcolor = property(_get_bgcolor, _set_bgcolor)


term = TerminalInfo()
term.bgcolor = 'black'
