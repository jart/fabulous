# Copyright 2016 The Fabulous Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import fabulous
from fabulous.color import *
from fabulous import text, utils, image, debug, xterm256


def wait():
    raw_input("\nPress " + bold("enter") + " for more fun... ")
    print ""


def demo_image():
    section("Semi-Transparent PNG")
    imp = "  from fabulous import image\n  "
    print bold(imp + 'print image.Image("balls.png")\n')

    balls = 'balls.png'
    fabdir = os.path.dirname(fabulous.__file__)

    for fn in ['balls.png',
               'fabulous/balls.png',
               os.path.join(fabdir, 'balls.png')]:
        if os.path.exists(fn):
            balls = fn
            break

    if not os.path.exists(balls):
        import urllib
        ugh = urllib.urlopen('http://lobstertech.com/media/img/balls.png')
        open('balls.png', 'w').write(ugh.read())
        balls = 'balls.png'

    for line in image.Image(balls):
        print line
    wait()

    section("Yes the output is optimized (JELLY-FISH)")
    imp = "  from fabulous import debug\n  "
    print bold(imp + 'print debug.DebugImage("balls.png")\n')
    for line in debug.DebugImage(balls):
        print line
    wait()


def demo_text():
    section('Fabulous Text Rendering')

    imp = "  from fabulous import text\n  "
    # print bold(imp + 'print text.Text("Fabulous")\n')
    # print text.Text("Fabulous")
    # wait()

    print bold(imp + 'print text.Text("Fabulous", shadow=True, skew=5)\n')
    print text.Text("Fabulous", shadow=True, skew=5)
    wait()


def demo_color_4bit():
    section("Fabulous 4-Bit Colors")

    print ("style(...): " +
           bold("bold") +" "+
           underline("underline") +" "+
           flip("flip") +
           " (YMMV: " + italic("italic") +" "+
           underline2("underline2") +" "+
            strike("strike") +" "+
           blink("blink") + ")\n").as_utf8

    print ("color(...)           " +
           black("black") +" "+
           red("red") +" "+
           green("green") +" "+
           yellow("yellow") +" "+
           blue("blue") +" "+
           magenta("magenta") +" "+
           cyan("cyan") +" "+
           white("white")).as_utf8

    print ("bold(color(...))     " +
           bold(black("black") +" "+
                red("red") +" "+
                green("green") +" "+
                yellow("yellow") +" "+
                blue("blue") +" "+
                magenta("magenta") +" "+
                cyan("cyan") +" "+
                white("white"))).as_utf8

    print plain(
        'highlight_color(...) ',
        highlight_black('black'), ' ', highlight_red('red'), ' ',
        highlight_green('green'), ' ', highlight_yellow('yellow'), ' ',
        highlight_blue('blue'), ' ', highlight_magenta('magenta'), ' ',
        highlight_cyan('cyan'), ' ', highlight_white('white')).as_utf8

    print ("bold(color_bg(...))  " +
           bold(black_bg("black") +" "+
                red_bg("red") +" "+
                green_bg("green") +" "+
                yellow_bg("yellow") +" "+
                blue_bg("blue") +" "+
                magenta_bg("magenta") +" "+
                cyan_bg("cyan") +" "+
                white_bg("white"))).as_utf8

    wait()


def demo_color_8bit():
    section("Fabulous 8-Bit Colors")

    for code in ["bold(fg256('red', ' lorem ipsum '))",
                 "bold(bg256('#ff0000', ' lorem ipsum '))",
                 "highlight256((255, 0, 0), ' lorem ipsum ')",
                 "highlight256('#09a', ' lorem ipsum ')",
                 "highlight256('green', ' lorem ipsum ')",
                 "highlight256('magenta', ' lorem ipsum ')",
                 "highlight256('indigo', ' lorem ipsum ')",
                 "highlight256('orange', ' lorem ipsum ')",
                 "highlight256('orangered', ' lorem ipsum ')"]:
        print "%-42s %s" % (code, eval(code))
    print ''

    # grayscales
    line = " "
    for xc in range(232, 256):
        line += bg256(xc, '  ')
    print line
    line = " "
    for xc in range(232, 256)[::-1]:
        line += bg256(xc, '  ')
    print line
    print ''

    cube_color = lambda x,y,z: 16 + x + y*6 + z*6*6
    for y in range(6):
        line = " "
        for z in range(6):
            for x in range(6):
                line += bg256(cube_color(x, y, z), '  ')
            line += " "
        print line.as_utf8

    wait()


def full_chart():
    # grayscales
    line = " "
    for xc in range(232, 256):
        line += bg256(xc, '  ')
    print line
    line = " "
    for xc in range(232, 256)[::-1]:
        line += bg256(xc, '  ')
    print line
    print ''

    # cube
    print ""
    cube_color = lambda x,y,z: 16 + x + y*6 + z*6*6
    for y in range(6):
        line = " "
        for z in range(6):
            for x in range(6):
                line += bg256(cube_color(x, y, z), '  ')
            line += " "
        print line.as_utf8
    print ""

    def f(xc):
        s = highlight256(xc, "color %03d" % (xc))
        rgb = xterm256.xterm_to_rgb(xc)
        rgbs = ' (%3d, %3d, %3d)' % rgb
        if rgb[0] == rgb[1] == rgb[2]:
            s += bold(rgbs)
        else:
            s += rgbs
        s += ' (%08d, %08d, %08d)' % tuple([int(bin(n)[2:]) for n in rgb])
        return s

    def l(c1, c2):
        c1, c2 = f(c1), f(c2)
        assert len(c1) == len(c2)
        half = width // 2
        assert half > len(c1)
        pad = " " * ((width // 2 - len(c1)) // 2)
        print "%(pad)s%(c1)s%(pad)s%(pad)s%(c2)s" % {'pad': pad, 'c1': c1, 'c2': c2}

    width = utils.term.width
    for z1, z2 in zip((0, 2, 4), (1, 3, 5)):
        for y1, y2 in zip(range(6), range(6)):
            for x1, x2 in zip(range(6), range(6)):
                l(cube_color(x1, y1, z1), cube_color(x2, y2, z2))
        print ""


def main():
    # full_chart()
    demo_color_4bit()
    demo_color_8bit()
    demo_text()
    demo_image()


if __name__ == '__main__':
    main()
