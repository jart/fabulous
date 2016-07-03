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
        print text.Text("Fabulous!", color='#0099ff', shadow=True, scew=5)

    To make things simple, Fabulous bundles three decent serif, sans-serif, and
    monospace fonts:

    - IndUni-H-Bold: Open Source Helvetica Bold clone (sans-serif)

      This is the real deal and not some cheap ripoff like Verdana.
      IndUni-H-Bold is the default because not only does it look
      great, but also renders *perfectly*.  and is also used for the
      Fabulous logo.  Commonly found on stret signs.

      This font is licensed under the GPL.  If you're developing
      proprietary software you might want to ask its author or a
      lawyer if Fabulous' use of IndUni-H would be considered a "GPL
      Barrier."

    - cmr10: Computer Modern (serif)

      Donald Knuth wrote 23,000 lines for the sole purpose of
      bestowing this jewel upon the world.  This font is commonly seen
      in scholarly papers.

    - DejaVuSansMono: DejaVu Sans Mono (formerly Bitstream Vera Sans Mono)

      At point size 8, this is my favorite programming/terminal font.

    For other fonts, Fabulous will do its best to figure out where they are
    stored. If Fabulous has trouble finding your font, try using an absolute
    path *with* the extension. It's also possible to put the font in the
    ``~/.fonts`` directory and then running ``fc-cache -fv ~/.fonts``.

"""

import os
import sys

from fabulous import utils, image, grapefruit


class Text(image.Image):
    """Renders TrueType Text to Terminal

    I'm a sub-class of :class:`fabulous.image.Image`.  My job is
    limited to simply getting things ready.  I do this by:

    - Turning your text into an RGB-Alpha bitmap image using
      :mod:`PIL`

    - Applying way cool effects (if you choose to enable them)

    For example::

        >>> assert Text("Fabulous", shadow=True, skew=5)

        >>> txt = Text("lorem ipsum", font="IndUni-H-Bold")
        >>> len(str(txt)) > 0
        True
        >>> txt = Text("lorem ipsum", font="cmr10")
        >>> len(str(txt)) > 0
        True
        >>> txt = Text("lorem ipsum", font="DejaVuSansMono")
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

    def __init__(self, text, fsize=20, color="#0099ff", shadow=False,
                 skew=None, font='IndUni-H-Bold'):
        utils.pil_check()
        from PIL import Image, ImageFont, ImageDraw
        self.text = text
        self.color = grapefruit.Color.NewFromHtml(color)
        self.font = ImageFont.truetype(resolve_font(font), fsize)
        size = tuple([n + 3 for n in self.font.getsize(self.text)])
        self.img = Image.new("RGBA", size, (0, 0, 0, 0))
        cvs = ImageDraw.Draw(self.img)
        if shadow:
            cvs.text((2, 2), self.text,
                     font=self.font,
                     fill=(150, 150, 150, 150))
        cvs.text((1, 1), self.text,
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
    """Sloppy way to turn font names into absolute filenames

    This isn't intended to be a proper font lookup tool but rather a
    dirty tool to not have to specify the absolute filename every
    time.

    For example::

        >>> path = resolve_font('IndUni-H-Bold')

        >>> fontdir = os.path.join(os.path.dirname(__file__), 'fonts')
        >>> indunih_path = os.path.join(fontdir, 'IndUni-H-Bold.otf')
        >>> assert path == indunih_path

    This isn't case-sensitive::

        >>> assert resolve_font('induni-h') == indunih_path

    Raises :exc:`FontNotFound` on failure::

        >>> resolve_font('blahahaha')
        Traceback (most recent call last):
        ...
        FontNotFound: Can't find 'blahahaha' :'(  Try adding it to ~/.fonts

    """
    for fontdir, fontfiles in get_font_files():
        for fontfile in fontfiles:
            if name.lower() in fontfile.lower():
                return os.path.join(fontdir, fontfile)
    raise FontNotFound("Can't find %r :'(  Try adding it to ~/.fonts" % name)


@utils.memoize
def get_font_files():
    """Returns a list of all font files we could find

    Returned as a list of dir/files tuples::

        get_font_files() -> [('/some/dir', ['font1.ttf', ...]), ...]

    For example::

        >>> fabfonts = os.path.join(os.path.dirname(__file__), 'fonts')
        >>> sorted(dict(get_font_files())[fabfonts])
        ['DejaVuSansMono.ttf', 'IndUni-H-Bold.otf', 'cmr10.ttf']

        >>> for dirname, filenames in get_font_files():
        ...     for filename in filenames:
        ...         assert os.path.exists(os.path.join(dirname, filename))
        ...

    """
    dirs = [os.path.join(os.path.dirname(__file__), 'fonts'),
            os.path.expanduser('~/.fonts')]

    sys_dirs = [
        # this is where ubuntu puts fonts
        '/usr/share/fonts/truetype',
        # this is where fedora puts fonts
        '/usr/share/fonts',
    ]

    for dirname in sys_dirs:
        try:
            dirs += [os.path.join(dirname, subdir)
                     for subdir in os.listdir(dirname)]
        except OSError:
            pass

    return [(p, os.listdir(p)) for p in dirs if os.path.isdir(p)]


def main():
    """Main function for :command:`fabulous-text`."""
    import optparse
    parser = optparse.OptionParser()
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
        "-F", "--font", dest="font", default='IndUni-H-Bold',
        help=("Path to font file you wish to use.  This defaults to a "
              "free Helvetica-Bold clone which is included with Fabulous.  "
              "Included fonts: IndUni-H-Bold, cmr10, DejaVuSansMono. "
              "Default: %default"))
    parser.add_option(
        "-Z", "--size", dest="fsize", type="int", default=20,
        help=("Size of font in points.  Default: %default"))
    parser.add_option(
        "-s", "--shadow", dest="shadow", action="store_true", default=False,
        help=("Size of font in points.  Default: %default"))
    (options, args) = parser.parse_args(args=sys.argv[1:])

    if options.term_color:
        utils.term.bgcolor = options.term_color

    for line in " ".join(args).split("\n"):
        fab_text = Text(line, skew=options.skew, color=options.color,
                        font=options.font, fsize=options.fsize,
                        shadow=options.shadow)
        for chunk in fab_text:
            print chunk


if __name__ == '__main__':
    main()
