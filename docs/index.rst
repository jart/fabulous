.. fabulous documentation master file, created by
   sphinx-quickstart on Tue Apr 20 02:12:28 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========
 Fabulous
==========

.. toctree::
   :maxdepth: 2

:Version: 0.2.1
:Founder: Justine Alexandra Roberts Tunney
:Copyright: Copyright 2016 The Fabulous Authors. All rights reserved.
:License: Apache 2.0 / OFL
:Support: Python 2.6, 2.7, 3.3, 3.4, 3.5, and pypy
:Source: `github.com/jart/fabulous`_

Fabulous is a Python library (and command line tools) designed to make the
output of terminal applications look *fabulous*. Fabulous allows you to print
colors, images, and stylized text to the console (without curses.)  Fabulous
also offers features to improve the usability of Python's standard logging
system.

.. _github.com/jart/fabulous: https://github.com/jart/fabulous


Installation
============

The following prerequisites should be installed, but they are not mandatory.
They help Fabulous run faster and make the full feature set available::

    sudo apt-get install gcc python-imaging

Fabulous can be installed from CheeseShop::

    sudo pip install fabulous

Fabulous can also be installed manually from the source archive::

    wget https://github.com/jart/fabulous/releases/download/0.2.1/fabulous-0.2.1.tar.gz
    tar -xvzf fabulous-0.2.1.tar.gz
    cd fabulous-0.2.1
    sudo python setup.py install

Once installed, run the demo::

    fabulous-demo

.. image:: images/fabulous-demo.png


Examples
========


Colors
------

4-bit colors and styles are standard and work almost everywhere. They are
useful in helping make your program output easier to read::

    from fabulous.color import bold, magenta, highlight_red

    print bold(magenta('hello world'))

    print highlight_red('DANGER WILL ROBINSON!')

    print bold('hello') + ' ' + magenta(' world')

    assert len(bold('test')) == 4

8-bit color works in most modern terminals, such as gnome-terminal and
Terminal.app::

    from fabulous import fg256, bg256
    print fg256('#F0F', 'hello world')
    print fg256('magenta', 'hello world')


Fancy Text
----------

This is something neat you can use when you program starts up to display its
name with style::

    from fabulous import text
    print text.Text("Fabulous!", color='#0099ff', shadow=True, skew=5)


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

Image printing may perform slowly depending on whether or not Fabulous is able
to compile ``~/.xterm256.so`` on the fly. This is a tiny library that makes
color quantization go much faster. The pure Python version of the algorithm is
really slow because it's implemented as a brute force nearest neighbor over
Euclidean distance search. Although an O(1) version of this algorithm exists
with slightly less correctness. Your humble author simply hasn't had the time
to implement it in this library.

If you like this image printing feature, then please check out hiptext_ which
is a C++ program written by the same author as Fabulous. It offers a much
richer version of this same functionality. It can even play videos in the
terminal. Also be sure to check out rickrollrc_.

.. _hiptext: https://github.com/jart/hiptext
.. _rickrollrc: https://github.com/keroserene/rickrollrc


Commands
========


fabulous-text
-------------

.. program-output:: fabulous-text --help


fabulous-image
--------------

.. program-output:: fabulous-image --help


fabulous-demo
-------------

Displays a demo showing what Fabulous can do.


fabulous-gotham
---------------

The :command:`fabulous-gotham` command is a gothic poetry generator. It is a
gimmick feature that uses a simple mad lib algorithm. It has no concept of
meter or rhyme. Users wanting a *proper* poetry generator should consider
poemy2_ which uses markov chains and isledict. It's also written by the same
author as Fabulous.

.. _poemy2: https://github.com/jart/poemy2


fabulous-rotatingcube
---------------------

The :command:`fabulous-rotatingcube` command is another gimmick feature that
animates a wireframe rotating cube in the terminal. It runs until you hit
Ctrl+C.


Library
=======

.. automodule:: fabulous.color
   :members:
.. automodule:: fabulous.xterm256
   :members:
.. automodule:: fabulous.text
   :members:
.. automodule:: fabulous.image
   :members:
.. automodule:: fabulous.logs
   :members:
.. automodule:: fabulous.widget
   :members:
.. automodule:: fabulous.term
   :members:
.. automodule:: fabulous.rlcomplete
   :members:
.. automodule:: fabulous.gotham
   :members:
.. automodule:: fabulous.rotating_cube
   :members:
.. automodule:: fabulous.debug
   :members:
.. automodule:: fabulous.utils
   :members:


Terminal Support
================

Supported Terminals
-------------------

===============  =======  =======  ===  =========  =======  =======  ======
Terminal         default  bright   dim  underline  blink    reverse  hidden
===============  =======  =======  ===  =========  =======  =======  ======
xterm            yes      yes      yes  yes        yes      yes      yes
linux            yes      yes      yes  bright     yes      yes      no
rxvt             yes      yes      no   yes        bright   yes      no
Windows [0]_     yes      yes      yes  no         no       yes      yes
PuTTY [1]_       yes      yes      no   yes        [2]_     yes      no
Cygwin SSH [3]_  yes      yes      no   [4]_       [4]_     [2]_     yes
===============  =======  =======  ===  =========  =======  =======  ======

Currently unsupported, but should support
-----------------------------------------

===============  =======  =======  ===  =========  =======  =======  ======
Terminal         default  bright   dim  underline  blink    reverse  hidden
===============  =======  =======  ===  =========  =======  =======  ======
dtterm           yes      yes      yes  yes        reverse  yes      yes
teraterm         yes      reverse  no   yes        rev/red  yes      no
aixterm          kinda    normal   no   yes        no       yes      yes
Mac Terminal     yes      yes      no   yes        yes      yes      yes
===============  =======  =======  ===  =========  =======  =======  ======

Unsupported and will not support
--------------------------------

Windows Telnet
	It thinks it supports ANSI control, but it's so horribly 
	buggy its best to ignore it all together. (``TERM = ansi``)


.. [0] The default windows terminal, ``cmd.exe`` does not set the ``TERM`` variable, so
	detection is done by checking if the string ``'win32'`` is in ``sys.platform``. This
	This method has some limitations, particularly with remote terminal. But if you're
	allowing remote access to a Windows computer you probably have bigger problems.
	
.. [1] Putty has the ``TERM`` variable set to ``xterm`` by default

.. [2] Makes background bright

.. [3] Cygwin's SSH support's ANSI, but the regular terminal does not, check for
	win32 first, then check for cygwin. That should give us the cases when
	cygwin is used through SSH or telnet or something. (``TERM = cygwin``)

.. [4] Sets foreground color to cyan


Alternatives
============

Here's how Fabulous compares to other similar libraries:

- fabulous_: Licensed Apache 2.0. Focuses on delivering useful features in the
  simplest, most user-friendly way possible (without a repulsive name.)
  Written in pure-python but will attempt to auto-magically compile/link a
  speedup library.  ~5,000 lines of code.

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


License
=======

Fabulous code and documentation are licensed Apache 2.0:

.. include:: ../LICENSE.txt
   :literal:

The bundled Google Noto Fonts are licensed under the SIL Open Font License,
Version 1.1:

.. include:: ../fabulous/fonts/LICENSE.txt
   :literal:
