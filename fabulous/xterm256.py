"""Implements Support for 256-color Terminals
"""

from grapefruit import Color


CUBE_STEPS = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
BASIC16 = ((0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
           (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
           (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
           (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255))


def xterm_to_rgb(xcolor):
    assert 0 <= xcolor <= 255
    if xcolor < 16:
        # basic colors
        return BASIC16[xcolor]
    elif 16 <= xcolor <= 231:
        # color cube
        xcolor -= 16
        return (CUBE_STEPS[(xcolor / 36) % 6],
                CUBE_STEPS[(xcolor / 6) % 6],
                CUBE_STEPS[xcolor % 6])
    elif 232 <= xcolor <= 255:
        # gray tone
        c = 8 + (xcolor - 232) * 0x0A
        return (c, c, c)
COLOR_TABLE = [xterm_to_rgb(i) for i in xrange(256)]


def rgb_to_xterm(color):
    if hasattr(color, 'rgb'):
        (r, g, b) = [int(round(c * 255.0)) for c in color.rgb]
    elif isinstance(color, basestring):
        (r, g, b) = [int(round(c * 255.0)) for c in Color.HtmlToRgb(color)]
    else:
        (r, g, b) = color
    best_match = 0
    smallest_distance = 10000000000
    for c in xrange(16, 256):
        d = (COLOR_TABLE[c][0] - r) ** 2 + \
            (COLOR_TABLE[c][1] - g) ** 2 + \
            (COLOR_TABLE[c][2] - b) ** 2
        if d < smallest_distance:
            smallest_distance = d
            best_match = c
    return best_match
