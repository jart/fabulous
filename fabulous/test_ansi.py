"""py.test ansi colorization
"""

from fabulous.ansi import *

def test_empty():
    c = bold()
    assert str(c) == ''

def test_magenta():
    c = magenta('yo yo yo')
    assert str(c) == '\x1b[35myo yo yo\x1b[0m'

def test_nested():
    c = bold(blue('hi'))
    assert str(c) == '\x1b[1;34mhi\x1b[0m'

def test_optimizer():
    c = blue(blue(blue("hi")))
    assert str(c) == '\x1b[34mhi\x1b[0m'

def test_parent_state_removal():
    c = bold(blue("before ", bold("hi"), " after"))
    assert str(c) == '\x1b[1;34mbefore hi after\x1b[0m'

def test_parent_state_reduction():
    c = bold(blue("before ", bold(green("hi")), " after"))
    assert str(c) == '\x1b[1;34mbefore \x1b[32mhi\x1b[34m after\x1b[0m'

def test_background_reset():
    c = bold(blue("before ", bold(green_bg("hi")), " after"))
    assert str(c) == '\x1b[1;34mbefore \x1b[42mhi\x1b[49m after\x1b[0m'

def test_parent_state_optimizer():
    c = blue(bold("omg"), " yep ", red("ha", underline("h"), "a"))
    assert str(c) == '\x1b[1;34momg\x1b[22m yep \x1b[31mha\x1b[4mh\x1b[24ma\x1b[0m'

def test_color_256():
    c = fg((123,70,255), "hello")
    assert str(c) == "\x1b[38;5;99mhello\x1b[0m"

def test_custom_color():
    """What the heck?  Why the hell does this happen:

    Above: rgb2xterm((123,70,225)) -> 99
    Here:  rgb2xterm((123,70,225)) -> 98 !!!
    """
    lawl = style(bold, blue, bg((123,70,225)))
    c = lawl("hello")
    assert str(c) == "\x1b[1;34;48;5;98mhello\x1b[0m"
