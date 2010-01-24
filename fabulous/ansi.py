"""ANSI Terminal Color Output Support
"""

import collections
from itertools import groupby


__all__ = ['bold', 'italic', 'underline', 'strike', 'flip', 'black', 'red',
           'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'black_bg',
           'red_bg', 'green_bg', 'yellow_bg', 'blue_bg', 'magenta_bg',
           'cyan_bg', 'white_bg', 'fg', 'bg', 'style', 'Fabulous']


class Fabulous(object):
    def __init__(self, *args):
        self.children = args

    def __str__(self):
        return "".join(_compile(_optimize(self)))

    def __unicode__(self):
        return "".join(_compile(_optimize(self)))

    def __repr__(self):
        return repr(str(self))

    def __iter__(self):
        yield self.codes
        for child in self.children:
            if hasattr(child, 'assemble'):
                for i in child.assemble(parent_codes=full_codes):
                    yield i
            else:
                yield child



class style(int):
    def __init__(self, ansi_id):
        self.group_ = 'style_%d' % (ansi_id)
        int.__init__(self, ansi_id)


class fgcolor(int):
    group_ = 'fg'


class bgcolor(int):
    group_ = 'bg'


class fgcolor256(fgcolor):
    def __str__(self):
        return "38;5;%d" % (self)


class bgcolor256(bgcolor):
    def __str__(self):
        return "48;5;%d" % (self)


class ANSIColorSet(collections.Set):
     def __init__(self, iterable):
         self.elements = {}
         for id_ in iterable:
             self.elements[v.group_] = id_

     def __iter__(self):
         return iter(self.elements.values())

     def __contains__(self, value):
         return value in self.elements

     def __len__(self):
         return len(self.elements)


class bold(Fabulous):       codes = ANSIColorSet([style(1)])
class italic(Fabulous):     codes = ANSIColorSet([style(3)])
class underline(Fabulous):  codes = ANSIColorSet([style(4)])
class strike(Fabulous):     codes = ANSIColorSet([style(9)])
class flip(Fabulous):       codes = ANSIColorSet([style(7)])

class black(Fabulous):      codes = ANSIColorSet([fgcolor(30)])
class red(Fabulous):        codes = ANSIColorSet([fgcolor(31)])
class green(Fabulous):      codes = ANSIColorSet([fgcolor(32)])
class yellow(Fabulous):     codes = ANSIColorSet([fgcolor(33)])
class blue(Fabulous):       codes = ANSIColorSet([fgcolor(34)])
class magenta(Fabulous):    codes = ANSIColorSet([fgcolor(35)])
class cyan(Fabulous):       codes = ANSIColorSet([fgcolor(36)])
class white(Fabulous):      codes = ANSIColorSet([fgcolor(37)])

class black_bg(Fabulous):   codes = ANSIColorSet([bgcolor(40)])
class red_bg(Fabulous):     codes = ANSIColorSet([bgcolor(41)])
class green_bg(Fabulous):   codes = ANSIColorSet([bgcolor(42)])
class yellow_bg(Fabulous):  codes = ANSIColorSet([bgcolor(43)])
class blue_bg(Fabulous):    codes = ANSIColorSet([bgcolor(44)])
class magenta_bg(Fabulous): codes = ANSIColorSet([bgcolor(45)])
class cyan_bg(Fabulous):    codes = ANSIColorSet([bgcolor(46)])
class white_bg(Fabulous):   codes = ANSIColorSet([bgcolor(47)])


class fg(Fabulous):
    def __init__(self, color, *args, **kwargs):
        color = fgcolor256(rgb2xterm(color))
        self.codes = self.codes.union(ANSIColorSet([color]))
        Fabulous.__init__(self, *args, **kwargs)


class bg(Fabulous):
    def __init__(self, color, *args, **kwargs):
        color = bgcolor256(rgb2xterm(color))
        self.codes = self.codes.union(ANSIColorSet([color]))
        Fabulous.__init__(self, *args, **kwargs)


def style(*args):
    """Creates a custom color class

    Example usage::

      keyword = style(bold, blue, bg((240,240,240)))
      print keyword("hello")

      print style(bold)("hello")
    """
    class custom_style(Fabulous):
        codes = ANSIColorSet([]).union(*[f.codes for f in args])
    return custom_style


def _optimize(fab):
    state = ANSIColorSet()
    for gtype, group in groupby(iter(fab), lambda i: type(i)):
        if issubclass(gtype, ANSIColorSet):
            res = ANSIColorSet()
            for s in group:
                res.update(s)
            if 0 in res:
                res = set([0])
            yield res
        elif issubclass(gtype, basestring):
            # this won't join bytestrings with unicode strings which
            # is *good* because encoding is compile()'s job
            x = list(group)
            yield "".join(x)
        else:
            for i in group:
                yield i


def _compile(fab):
    """Generator that turns sets into ANSI escape codes.

    Example::

      [set([1, 34]), "i am blue!!!", set([0])]
      -> ["\x1b[1;34m", "i am blue!!!", "\x1b[0m"]
    """
    for item in fab:
        if type(item) is set:
            yield "\x1b[%sm" % (";".join([str(c) for c in item]))
        else:
            yield item


def _ansi_reverse(c):
    if hasattr(c, '__iter__'):
        return set([_ansi_reverse(i) for i in c])
    else:
        if isinstance(c, fgcolor):
            return 39 # ansi reset fg
        elif isinstance(c, bgcolor):
            return 49 # ansi reset bg
        else:
            return {1:22, 3:23, 4:24, 9:29, 7:27,
                    22:1, 23:3, 24:4, 29:9, 27:7}[c]
