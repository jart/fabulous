# -*- coding: utf-8 -*-
#
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

"""
    fabulous.text
    ~~~~~~~~~~~~~

    The text module makes it possible to print TrueType text to the terminal.
    This functionality is available on the command line::

        jart@compy:~$ fabulous-text --help
        jart@compy:~$ fabulous-text --skew=5 --shadow 'Fabulous!'
        jart@compy:~$ python -m fabulous.text --help

    Or as a Python library:

    .. code-block:: python

        from fabulous import text
        print text.Text("Fabulous!", color='#0099ff', shadow=True, skew=5)

    To make things simple, Fabulous bundles the following Google Noto Fonts
    which look good and are guaranteed to work no matter what:

    - NotoSans-Bold
    - NotoEmoji-Regular

    For other fonts, Fabulous will do its best to figure out where they are
    stored. If Fabulous has trouble finding your font, try using an absolute
    path *with* the extension. It's also possible to put the font in the
    ``~/.fonts`` directory and then running ``fc-cache -fv ~/.fonts``.

    You can run ``fabulous-text --list`` to see what fonts are available.

"""

from __future__ import print_function

import os
import sys

from fabulous import utils, image, grapefruit
from fabulous.compatibility import printy

try:
    unicode = unicode
except NameError:
    unicode = str
    basestring = (str, bytes)


class Text(image.Image):
    u"""Renders TrueType Text to Terminal

    I'm a sub-class of :class:`fabulous.image.Image`.  My job is
    limited to simply getting things ready.  I do this by:

    - Turning your text into an RGB-Alpha bitmap image using
      :mod:`PIL`

    - Applying way cool effects (if you choose to enable them)

    For example::

        >>> assert Text("Fabulous", shadow=True, skew=5)

        >>> txt = Text("lorem ipsum", font="NotoSans-Bold")
        >>> len(str(txt)) > 0
        True
        >>> txt = Text(u"😃", font="NotoSans-Bold")
        >>> len(str(txt)) > 0
        True

    :param text:   The text you want to display as a string.

    :param fsize:  The font size in points.  This obviously end up
                   looking much larger because in fabulous a single
                   character is treated as one horizontal pixel and two
                   vertical pixels.

    :param color:  The color (specified as you would in HTML/CSS) of
                   your text.  For example Red could be specified as
                   follows: ``red``, ``#00F`` or ``#0000FF``.

    :param shadow: If true, render a simple drop-shadow beneath text.
                   The Fabulous logo uses this feature.

    :param skew:   Skew size in pixels.  This applies an affine
                   transform to shift the top-most pixels to the right.
                   The Fabulous logo uses a five pixel skew.

    :param font:   The TrueType font you want.  If this is not an
                   absolute path, Fabulous will search for your font by
                   globbing the specified name in various directories.
    """

    def __init__(self, text, fsize=23, color="#0099ff", shadow=False,
                 skew=None, font='NotoSans-Bold'):
        utils.pil_check()
        from PIL import Image, ImageFont, ImageDraw
        self.text = text
        self.color = grapefruit.Color.NewFromHtml(color)
        self.font = ImageFont.truetype(resolve_font(font), fsize)
        skew = skew or 0
        size = tuple([n + 3 + skew for n in self.font.getsize(self.text)])
        self.img = Image.new("RGBA", size, (0, 0, 0, 0))
        cvs = ImageDraw.Draw(self.img)
        if shadow:
            cvs.text((2 + skew, 2), self.text,
                     font=self.font,
                     fill=(150, 150, 150, 150))
        cvs.text((1 + skew, 1), self.text,
                 font=self.font,
                 fill=self.color.html)
        if skew:
            self.img = self.img.transform(
                size, Image.AFFINE, (1.0, 0.1 * skew, -1.0 * skew,
                                     0.0, 1.0, 0.0))
        self.resize(None)


class FontNotFound(ValueError):
    """I get raised when the font-searching hueristics fail

    This class extends the standard :exc:`ValueError` exception so you
    don't have to import me if you don't want to.
    """


def resolve_font(name):
    """Turns font names into absolute filenames

    This is case sensitive. The extension should be omitted.

    For example::

        >>> path = resolve_font('NotoSans-Bold')

        >>> fontdir = os.path.join(os.path.dirname(__file__), 'fonts')
        >>> noto_path = os.path.join(fontdir, 'NotoSans-Bold.ttf')
        >>> noto_path = os.path.abspath(noto_path)
        >>> assert path == noto_path

    Absolute paths are allowed::

        >>> resolve_font(noto_path) == noto_path
        True

    Raises :exc:`FontNotFound` on failure::

        >>> try:
        ...     resolve_font('blahahaha')
        ...     assert False
        ... except FontNotFound:
        ...     pass

    """
    if os.path.exists(name):
        return os.path.abspath(name)
    fonts = get_font_files()
    if name in fonts:
        return fonts[name]
    raise FontNotFound("Can't find %r :'(  Try adding it to ~/.fonts" % name)


@utils.memoize
def get_font_files():
    """Returns a list of all font files we could find

    Returned as a list of dir/files tuples::

        get_font_files() -> {'FontName': '/abs/FontName.ttf', ...]

    For example::

        >>> fonts = get_font_files()
        >>> 'NotoSans-Bold' in fonts
        True
        >>> fonts['NotoSans-Bold'].endswith('/NotoSans-Bold.ttf')
        True

    """
    roots = [
        '/usr/share/fonts/truetype',     # where ubuntu puts fonts
        '/usr/share/fonts',              # where fedora puts fonts
        os.path.expanduser('~/.fonts'),  # custom user fonts
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts')),
    ]
    result = {}
    for root in roots:
        for path, dirs, names in os.walk(root):
            for name in names:
                if name.endswith(('.ttf', '.otf')):
                    result[name[:-4]] = os.path.join(path, name)
    return result


def main():
    """Main function for :command:`fabulous-text`."""
    import optparse
    parser = optparse.OptionParser()
    parser.add_option(
        "-l", "--list", dest="list", action="store_true", default=False,
        help=("List available fonts"))
    parser.add_option(
        "-S", "--skew", dest="skew", type="int", default=None,
        help=("Apply skew effect (measured in pixels) to make it look "
              "extra cool.  For example, Fabulous' logo logo is skewed "
              "by 5 pixels.  Default: %default"))
    parser.add_option(
        "-C", "--color", dest="color", default="#0099ff",
        help=("Color of your text.  This can be specified as you would "
              "using HTML/CSS.  Default: %default"))
    parser.add_option(
        "-B", "--term-color", dest="term_color", default=None,
        help=("If you terminal background isn't black, please change "
              "this value to the proper background so semi-transparent "
              "pixels will blend properly."))
    parser.add_option(
        "-F", "--font", dest="font", default='NotoSans-Bold',
        help=("Name of font file, or absolute path to one. Use the --list "
              "flag to see what fonts are available. Fabulous bundles the "
              "NotoSans-Bold and NotoEmoji-Regular fonts, which are guaranteed "
              "to work. Default: %default"))
    parser.add_option(
        "-Z", "--size", dest="fsize", type="int", default=23,
        help=("Size of font in points.  Default: %default"))
    parser.add_option(
        "-s", "--shadow", dest="shadow", action="store_true", default=False,
        help=("Size of font in points.  Default: %default"))
    (options, args) = parser.parse_args(args=sys.argv[1:])
    if options.list:
        print("\n".join(sorted(get_font_files())))
        return
    if options.term_color:
        utils.term.bgcolor = options.term_color
    text = " ".join(args)
    if not isinstance(text, unicode):
        text = text.decode('utf-8')
    for line in text.split("\n"):
        fab_text = Text(line, skew=options.skew, color=options.color,
                        font=options.font, fsize=options.fsize,
                        shadow=options.shadow)
        for chunk in fab_text:
            printy(chunk)


if __name__ == '__main__':
    main()
