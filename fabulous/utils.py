
import fcntl
import struct
import termios


def term_width():
    call = fcntl.ioctl(0, termios.TIOCGWINSZ, "\000" * 8)
    height, width = struct.unpack("hhhh", call)[:2]
    return width
