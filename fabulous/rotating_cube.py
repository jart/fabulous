"""
    fabulous.rotating_cube
    ~~~~~~~~~~~~~~~~~~~~~~

    Command for animating a wireframe rotating cube in the terminal.

"""

from __future__ import with_statement

import sys
import time
from math import cos, sin, pi

from fabulous import color, utils


class Frame(object):
    """Canvas object for drawing a frame to be printed
    """

    def __enter__(self):
        self.width = utils.term.width
        self.height = utils.term.height * 2
        self.canvas = [[' ' for x in range(self.width)]
                       for y in range(self.height // 2)]
        return self

    def __exit__(self, type_, value, traceback):
        sys.stdout.write(self.render())
        sys.stdout.flush()

    def __setitem__(self, p, c):
        (x, y) = p
        self.canvas[int(y // 2)][int(x)] = c

    def line(self, x0, y0, x1, y1, c='*'):
        r"""Draws a line

        Who would have thought this would be so complicated?  Thanks
        again Wikipedia_ <3

        .. _Wikipedia: http://en.wikipedia.org/wiki/Bresenham's_line_algorithm
        """
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            (x0, y0) = (y0, x0)
            (x1, y1) = (y1, x1)
        if x0 > x1:
            (x0, x1) = (x1, x0)
            (y0, y1) = (y1, y0)
        deltax = x1 - x0
        deltay = abs(y1 - y0)
        error = deltax / 2
        y = y0
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        for x in range(x0, x1 - 1):
            if steep:
                self[y, x] = c
            else:
                self[x, y] = c
            error = error - deltay
            if error < 0:
                y = y + ystep
                error = error + deltax

    def render(self):
        return "\n".join(["".join(line) for line in self.canvas])


def rotating_cube(degree_change=3, frame_rate=3):
    """Rotating cube program

    How it works:

      1. Create two imaginary ellipses
      2. Sized to fit in the top third and bottom third of screen
      3. Create four imaginary points on each ellipse
      4. Make those points the top and bottom corners of your cube
      5. Connect the lines and render
      6. Rotate the points on the ellipses and repeat

    """
    degrees = 0
    while True:
        t1 = time.time()

        with Frame() as frame:
            oval_width = frame.width
            oval_height = frame.height / 3.0
            cube_height = int(oval_height * 2)

            (p1_x, p1_y) = ellipse_point(degrees, oval_width, oval_height)
            (p2_x, p2_y) = ellipse_point(degrees + 90, oval_width, oval_height)
            (p3_x, p3_y) = ellipse_point(degrees + 180, oval_width, oval_height)
            (p4_x, p4_y) = ellipse_point(degrees + 270, oval_width, oval_height)
            degrees = (degrees + degree_change) % 360

            # connect square thing at top
            frame.line(p1_x, p1_y, p2_x, p2_y)
            frame.line(p2_x, p2_y, p3_x, p3_y)
            frame.line(p3_x, p3_y, p4_x, p4_y)
            frame.line(p4_x, p4_y, p1_x, p1_y)

            # connect top to bottom
            frame.line(p1_x, p1_y, p1_x, p1_y + cube_height)
            frame.line(p2_x, p2_y, p2_x, p2_y + cube_height)
            frame.line(p3_x, p3_y, p3_x, p3_y + cube_height)
            frame.line(p4_x, p4_y, p4_x, p4_y + cube_height)

            # connect square thing at bottom
            frame.line(p1_x, p1_y + cube_height, p2_x, p2_y + cube_height)
            frame.line(p2_x, p2_y + cube_height, p3_x, p3_y + cube_height)
            frame.line(p3_x, p3_y + cube_height, p4_x, p4_y + cube_height)
            frame.line(p4_x, p4_y + cube_height, p1_x, p1_y + cube_height)

        elapsed = (time.time() - t1)
        time.sleep(abs(1.0 / frame_rate - elapsed))


def ellipse_point(degrees, width, height):
    width -= 1
    height -= 1
    radians = degrees * (pi / 180.0)
    x = width/2.0 * cos(1) * sin(radians) - width/2.0 * sin(1) * cos(radians)
    y = height/2.0 * sin(1) * sin(radians) + height/2.0 * cos(1) * cos(radians)
    x = int(x + width/2.0)
    y = int(y + height/2.0)
    return (x, y)


def main():
    try:
        rotating_cube()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
