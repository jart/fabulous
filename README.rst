.. -*-restructuredtext-*-

==========
 Fabulous
==========

---------------------------------------------
 Makes Your Terminal Output Totally Fabulous
---------------------------------------------

:Version: 0.1.6
:Copyright: Copyright (c) 2009-2016 Justine Tunney
:Manual section: 3
:Manual group: Library Calls


Getting Started
===============

Download and extract the latest version::

  sudo apt-get install gcc python-imaging python-setuptools
  sudo python setup.py install

Run the demo to see what's available::

  python -m fabulous.demo


Basic Examples
==============

Colors
------

4-bit color.  These colors and styles are standard and work almost
everywhere.  They are useful in helping make your program output
easier to read::

  from fabulous import bold, magenta, highlight_red

  print bold(magenta('hello kitty'))
  print highlight_red('DANGER DANGER!')

  print bold('hello') + ' ' + magenta( kitty')

  assert len(bold('test')) == 4

8-bit color.  If you want to spice things up a bit, Fabulous supports
xterm256 colors::

  from fabulous import fg256, bg256
  print fg256('#F0F', 'hello kitty')
  print fg256('magenta', 'hello kitty')


Fancy Text
----------

Way cool text.  This is something neat you can use when you program
starts up to display its name with style::

  from fabulous import text
  print text.Text("Fabulous", color='#0099ff', shadow=True, scew=5)


Images
------

Fabulous lets you print images, which is more fun than useful.
Fabulous' unique method of printing images really shines when used
with semi-transparent PNG files.  When blending backgrounds, Fabulous
assumes by default that your terminal has a black background.  Don't
worry if your image is huge, it'll be resized by default to fit your
terminal::

  from fabulous import utils, image
  print image.Image("balls.png")

  # adjust for a white background
  utils.term.bgcolor = 'white'
  print image.Image("balls.png")

It's scriptable too (like img2txt) ::

  python -m fabulous.image balls.png >balls.txt
  cat balls.txt


Transient Logging
-----------------

This is very useful tool for monitoring what your Python scripts are
doing.  It allows you to have full verbosity without drowning out
important error messages::

  import time, logging
  from fabulous import logs
  logs.basicConfig(level='WARNING')

  for n in range(20):
      logging.debug("verbose stuff you don't care about")
      time.sleep(0.1)
  logging.warning("something bad happened!")
  for n in range(20):
      logging.debug("verbose stuff you don't care about")
      time.sleep(0.1)


Why Fabulous?
=============

Here's how Fabulous compares to other similar libraries:

- fabulous_: Licensed MIT.  Focuses on delivering useful features in
  the simplest, most user-friendly way possible (without a repulsive
  name.)  Written in pure-python but will attempt to auto-magically
  compile/link a speedup library.  ~1,000 lines of code.

- libcaca_: WTFPL.  This is the established and respected standard for
  doing totally insane things with ascii art (ever wanted to watch a
  movie on the command line?)  Weighing in at ~72k lines of C, this
  project is a monster.  It uses an older, more complex
  text/dithering-based rendering method.  Compared to fabulous, some
  images look better, some worse.  I found the docs somewhat difficult
  to follow and couldn't find support for transparency or 256-colors.

- asciiporn_: GPL.  Similar to libcaca but has an interesting feature
  for drawing math graphs to the terminal...  Needs to compile C code,
  requires numpy/python2.6, and I couldn't get the darn thing to work.
  Aprox 17k lines of code.

- pygments_: BSD.  Has *excellent* support for terminal syntax highlighting.

- termcolor_: GPL.  Only supports 4-bit ANSI colors.

.. _fabulous: http://pypi.python.org/pypi/fabulous
.. _libcaca: http://caca.zoy.org/
.. _termcolor: http://pypi.python.org/pypi/termcolor
.. _pygments: http://pygments.org/
.. _asciiporn: http://pypi.python.org/pypi/asciiporn/2009.05.01


ToDo
====

- <http://www.burgaud.com/bring-colors-to-the-windows-console-with-python/>
