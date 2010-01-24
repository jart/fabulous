"""Implements Support for 256-color Terminals
"""

import colorsys


CUBE_STEPS = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
BASIC16 = ((0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
           (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
           (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
           (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255))


def xterm_to_rgb(color):
    if color < 16:
        # basic colors
        return BASIC16[color]
    elif 16 <= color <= 232:
        # color cube
        color -= 16
        return (CUBE_STEPS[(color / 36) % 6],
                CUBE_STEPS[(color / 6) % 6],
                CUBE_STEPS[color % 6])
    elif 233 <= color <= 253:
        # gray tone
        c = 8 + (color - 232) * 0x0A
        return (c, c, c)
    else:
        assert False
COLOR_TABLE = [xterm_to_rgb(i) for i in xrange(254)]


def rgb_to_xterm(rgb):
    rgb = parse_rgb(rgb)
    best_match = 0
    smallest_distance = 10000000000
    for c in xrange(254):
        d = (COLOR_TABLE[c][0] - rgb[0]) ** 2 + \
            (COLOR_TABLE[c][1] - rgb[1]) ** 2 + \
            (COLOR_TABLE[c][2] - rgb[2]) ** 2
        if d < smallest_distance:
            smallest_distance = d
            best_match = c
    return best_match


def rgb_complement(rgb):
    rgb = parse_rgb(rgb)


def parse_rgb(color):
    """Turns various input formats into an RGB tuple

    >>> parse_rgb('#ff0000')
    (255, 0, 0)
    >>> parse_rgb('#f00')
    (255, 0, 0)
    >>> parse_rgb((255, 0, 0))
    (255, 0, 0)
    >>> parse_rgb((255, 0, 0, 255))
    (255, 0, 0)
    >>> parse_rgb((255, 0, 0, 0))
    (0, 0, 0)
    """
    if isinstance(color, basestring):
        if color.startswith('#'):
            color = color[1:]
        if len(color) == 3:
            color = "".join([c * 2 for c in color])
        return (int(color[:2], base=16),
                int(color[2:4], base=16),
                int(color[4:6], base=16))
    else:
        if len(color) == 3:
            return color
        elif len(color) == 4:
            # channel 4 = alpha
            # let's assume terminal background is black lol
            return rgb_alpha_to_black(color)
        else:
            assert False


def rgb_alpha_to_black(color):
    assert len(color) == 4
    if color[3] <= 0.001:
        return (0, 0, 0)
    elif color[3] >= 0.999:
        return color[:3]
    else:
        rgba_f = [float(c) / 255.0 for c in color]
        hsv_f = colorsys.rgb_to_hsv(*rgba_f[:3])
        hsv_f = (hsv_f[0], hsv_f[1], hsv_f[2] * rgba_f[3])
        rgb_f = colorsys.hsv_to_rgb(*hsv_f)
        rgb = [int(round(c * 255.0)) for c in color]
        return rgb

