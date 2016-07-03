.. -*-restructuredtext-*-

===================
 Fabulous |travis|
===================

.. |TRAVIS| image:: https://travis-ci.org/jart/fabulous.png?branch=master
           :target: https://travis-ci.org/jart/fabulous

Fabulous is a Python library (and command line tools) designed to make the
output of terminal applications look *fabulous*. Fabulous allows you to print
colors, images, and stylized text to the console (without curses.)  Fabulous
also offers features to improve the usability of Python's standard logging
system.


Installation
============

The following prerequisites are optional. But they help Fabulous run faster and
make the full feature set is available::

  sudo apt-get install gcc python-imaging

You can install Fabulous from PyPi::

  sudo pip install fabulous

Or you could download and extract the latest version::

  sudo python setup.py install

Run the demo to see what's available::

  fabulous-demo

.. image:: https://raw.githubusercontent.com/jart/fabulous/master/docs/fabulous-demo.png


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
  print text.Text("Fabulous!", color='#0099ff', shadow=True, scew=5)

It's scriptable too::

  fabulous-text --help
  fabulous-text --skew=5 --shadow 'Fabulous!'


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

  fabulous-image balls.png

Image printing may perform slowly depending on whether or not Fabulous is able
to compile `~/.xterm256.so` on the fly. This is a tiny library that makes color
quantization go much faster. The pure Python version of the algorithm is really
slow because it's implemented as a brute force nearest neighbor over Euclidean
distance search. Although an O(1) version of this algorithm exists with
slightly less correctness. Your humble author simply hasn't had the time to
implement it in this library.

If you like this image printing feature, then please check out hiptext_ which
is a C++ program written by the same author as Fabulous. It offers a much
richer version of this same functionality. It can even play videos in the
terminal. Also be sure to check out rickrollrc_.

.. _hiptext: https://github.com/jart/hiptext
.. _rickrollrc: https://github.com/keroserene/rickrollrc


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


Gothic Poetry Generator
-----------------------

This is a gimmick feature that probably shouldn't have been included, but it's
possible to generate silly gothic poetry by running ``fabulous-gotham``.

This uses a simple mad lib algorithm. It has no concept of meter or rhyme. If
you want a *proper* poetry generator, check out poemy2_ which uses markov
chains and isledict. It's written by the same author as Fabulous.

.. _poemy2: https://github.com/jart/poemy2


Rotating Cube
-------------

This is another gimmick feature that probably shouldn't have been included.
You can display an animated rotating cube in your terminal by running
``fabulous-rotatingcube``.


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
