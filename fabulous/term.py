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
    fabulous.term
    ~~~~~~~~~~~~~

    Terminal abstraction layer.

    Provides standard capabilites to a variety of terminals. Support information
    is being worked on.

    .. code-block:: python

        import os
        os.stdout.write('spam' +
                        display('bright','yellow','white') +
                        'eggs' +
                        display('default') + os.linesep)

    **Warning:** on IPython setting sys.stdout to stdout will break readline

    **Caveat:** Failure to flush after ouput can cause weird ordering behaviour
    when writing to stdout and stderr simutaniously. This should fix the worst
    of it, but application developers should be warned not to rely on the state
    of things between call between one method call and another

"""

__all__ = ['display', 'stdin', 'stdout', 'stderr',
           'Term', 'UnixTerm', 'CursesTerm',
           'WinTerm', 'Win32Term', 'WinCTypesTerm']

import sys
import os
import re

try:
    unicode = unicode
except NameError:
    unicode = str
    basestring = (str, bytes)


# pylint: disable-msg=W0613
# pylint: disable-msg=W0102
# pylint: disable-msg=C0103
# pylint: disable-msg=W0142
# pylint: disable-msg=R0201
# pylint: disable-msg=W0511

class Term(object):
    """A file-like object which also supports terminal features.
    
    This is a base class for dumb terminals. It supports almost nothing.
    """
    
    def __init__(self, stream):
        """Under Construction (:P)
        
        When overriding this in subclasses, please call
        Term.__init__(self, stream) first.
        
        Class specific imports are being done in the contructors and
        references to the modules are stored as instance variables. This
        method is cleaner and works nicely with inheritance.
        """
        self.stream = stream
    
    def bell(self):
        """Causes the computer to beep
        
        Use sparingly, it is mainly
        to alert the user if something potentialy bad may be happening.
        """
        pass
    
    def display(self, codes=[], fg=None, bg=None):
        """Not for public consumption (yet)
        
        Just use display() and stdout.write() for now.
        
        run this at the beginning::
        
            (codes, fg, bg) = Magic.displayformat(codes, fg, bg)
        """
        pass
    
    def move(self, place, distance = 1):
        """Move cursor position
        
        The valid values for place are:
        
        up
            Move up a line.
        down
            Move to the next line. This also puts you at the beginning of
            the line.
        left
            Move one place to the left.
        right
            Move one place to the right.
        beginning of line
            Move to the beginning of the current line.
        beginning of screen
            Move to the beginning of the screen.
        """
        pass
    
    def clear(self, scope = 'screen'):
        """clears part of the screen
        
        The valid values for scope are:
        
        right
            Clears a single space directly to the right.
        left
            Clears a single space directly to the left.
        line
            Clears the current line.
        screen
            Clears the whole screen.
        beginning of line
            Clears from the current position to the beginning of the line
        end of line
            Clears from the current position to the end of the line
        end of screen
            Clears from the current position to the end of the screen
        
        N.b. this is not the same as deleting. After a place is cleared
        it should still be there, but with nothing in it. Also, this
        should not change the position of the cursor.
        """
        pass
    
    def get_size(self):
        """Get the width and height of the terminal.
        
        Returns either a tuple of two integers or None. If two integers are
        returned, the first one is the number of columns (or width) and the
        second value is the number of lines (or height). If None is returned,
        then the terminal does not support this feature. If you still need to
        have a value to fall back on (75, 25) is a fairly descent fallback.
        """
        return None
    
    def set_title(self, name):
        """Sets the title of the terminal
        """
        pass
    
    # methods below here are also methods of the file object
    
    def isatty(self):
        """Returns True if the terminal is a terminal
        
        This should always be True. If it's not somebody is being rather
        nauty.
        """
        return self.stream.isatty()
    
    def fileno(self):
        """Returns the stream's file descriptor as an integer"""
        return self.stream.fileno()
    
    # write-specific methods
    
    def write(self, text):
        """Parses text and prints proper output to the terminal
        
        This method will extract escape codes from the text and
        handle them as well as possible for whichever platform
        is being used. At the moment only the display escape codes
        are supported.
        """
        escape_parts = re.compile('\x01?\x1b\\[([0-9;]*)m\x02?')
        chunks = escape_parts.split(text)
        i = 0
        for chunk in chunks:
            if chunk != '':
                if i % 2 == 0:
                    self.stream.write(chunk)
                else:
                    c = chunk.split(';')
                    r = Magic.rdisplay(c)
                    self.display(**r) #see caveat 0
                self.flush()
            i += 1
    
    def writelines(self, sequence_of_strings):
        """Write out a sequence of strings
        
        Note that newlines are not added.  The sequence may be any iterable object
        producing strings. This is equivalent to calling write() for each string.
        """
        map(self.write, sequence_of_strings)
    
    def flush(self):
        """Ensure the text is ouput to the screen.
        
        The write() method will do this automatically, so only use this when
        using self.stream.write().
        """
        return self.stream.flush()
    
    # read-specific methods, they are in need of help
    
    def getch(self):
        """Don't use this yet
        
        It doesn't belong here but I haven't yet thought about a proper
        way to implement this feature and the features that will depend on
        it.
        """
        pass
    
    def raw_input(self, prompt):
        """Don't use this yet
        
        It doesn't belong here but I haven't yet thought about a proper
        way to implement this feature and the features that will depend on
        it.
        """
        return raw_input(prompt)
    
    def next(self):
        return self.stream.next()
    
    def readline(self, *args, **kwargs):
        return self.stream.readline(*args, **kwargs)
    def readlines(self, *args, **kwargs):
        return self.stream.readlines(*args, **kwargs)
    def read(self, *args, **kwargs):
        return self.stream.read(*args, **kwargs)
    
    # read-only properties
    @property
    def mode(self):
        return self.stream.mode
    @property
    def newlines(self):
        return self.stream.newlines
    @property
    def encoding(self):
        return self.stream.encoding
    @property
    def softspace(self):
        return self.stream.softspace
    @property
    def name(self):
        return self.stream.name

class UnixTerm(Term):
    
    def __init__(self, stream):
        import termios
        import tty
        self.termios = termios
        self.tty = tty
        Term.__init__(self, stream)
    
    def getch(self):
        """Don't use this yet
        
        It doesn't belong here but I haven't yet thought about a proper
        way to implement this feature and the features that will depend on
        it.
        """
        return NotImplemented
        fno = stdout.fileno()
        mode = self.termios.tcgetattr(fno)
        try:
            self.tty.setraw(fno, self.termios.TCSANOW)
            ch = self.read(1)
        finally:
            self.termios.tcsetattr(fno, self.termios.TCSANOW, mode)
        return ch

class CursesTerm(UnixTerm):
    
    def __init__(self, stream):
        import curses
        self.curses = curses
        UnixTerm.__init__(self, stream)
        if not sys.stdout.isatty(): return
        self.curses.setupterm()
    
    def bell(self):
        self.stream.write(self._get_cap('bel'))
    
    def display(self, codes=[], fg=None, bg=None):
        """Displays the codes using ANSI escapes
        """
        codes, fg, bg = Magic.displayformat(codes, fg, bg)
        self.stream.write(Magic.display(codes, fg, bg))
        self.flush()
        
    def move(self, place, distance = 1):
        """see doc in Term class"""
        for d in range(distance):
            self.stream.write(self._get_cap('move '+place))
        self.flush()
    
    def clear(self, scope = 'screen'):
        """see doc in Term class"""
        if scope == 'line':
            self.clear('beginning of line')
            self.clear('end of line')
        else: self.stream.write(self._get_cap('clear '+scope))
        self.flush()
    
    def get_size(self):
        """see doc in Term class"""
        self.curses.setupterm()
        return self.curses.tigetnum('cols'), self.curses.tigetnum('lines')
    
    def set_title(self, name):
        self.write(Magic.OSC + '0;'+str(name) + "\x07") 
    
    def _get_cap(self, cap):
        strcaps = {
       'move up':'cuu1', 'move down':'cud1', 
           'move left':'cub1', 'move right':'cuf1',
           'move beginning of line':'cr', 'move beginning of screen':'home',
       'clear beginning of line':'el1','clear end of line':'el',
           'clear screen':'clear', 'clear end of screen':'ed',
           'clear left':'kbs','clear right':'dch1',
       'delete line':'dl1',
       'bell':'bel'}
        if cap in ('cols','lines'):
            self.curses.setupterm()
            c = self.curses.tigetnum(cap)
            if c > 0: return c
        elif strcaps.has_key(cap):
            c = self.curses.tigetstr(strcaps[cap])
            if c != '': return c
        raise ValueError("capability '%s' not supported" % cap)
    

class WinTerm(Term):
    """Windows version of terminal control
    
    This class should not be used by itself, use either Win32Terminal or 
    WinCTypesTerminal classes that subclasses of this class.
    
    This class makes extensive use of the Windows API
    
    The official documentation for the API is on MSDN (look for 'console
    functions')
    """
    
    # TODO: is there a better way to get this?
    
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    
    # These contants are defined in PyWin32
    # You can combine the values by doing a bitwise or (|)
    # for example FG_BLUE | FG_RED would give magenta (0x05)
    #
    # these contants are just numbers, It's most useful to think of
    # them in binary
    FG_BLUE = 1 << 0
    FG_GREEN = 1 << 1
    FG_RED = 1 << 2
    FG_INTENSITY = 1 << 3
    BG_BLUE = 1 << 4
    BG_GREEN = 1 << 5
    BG_RED = 1 << 6
    BG_INTENSITY = 1 << 7
    FG_ALL = FG_BLUE | FG_GREEN | FG_RED
    BG_ALL = BG_BLUE | BG_GREEN | BG_RED
    
    # there are also these codes, but according to tcsh's win32/console.c:
    # COMMON_LVB_REVERSE_VIDEO is buggy, so I'm staying away from it. Future
    # versions should implement COMMON_LVB_UNDERSCORE.
    # COMMON_LVB_REVERSE_VIDEO = 0x4000
    # COMMON_LVB_UNDERSCORE      0x8000
    
    FG = {
    'black': 0,
    'red': FG_RED,
    'green': FG_GREEN,
    'yellow': FG_GREEN | FG_RED,
    'blue': FG_BLUE,
    'magenta': FG_BLUE | FG_RED,
    'cyan': FG_BLUE | FG_GREEN,
    'white': FG_BLUE | FG_GREEN | FG_RED,
    }
    BG = {
    'black':0,
    'red':BG_RED,
    'green':BG_GREEN,
    'yellow':BG_GREEN | BG_RED,
    'blue':BG_BLUE,
    'magenta':BG_BLUE | BG_RED,
    'cyan':BG_BLUE | BG_GREEN,
    'white':BG_BLUE | BG_GREEN | BG_RED,
    }
    
    default_attributes = None
    hidden_output = False
    reverse_output = False
    reverse_input = False
    dim_output = False
    real_fg = None
    
    def __init__(self, stream):
        import msvcrt
        self.msvcrt = msvcrt
        Term.__init__(self, stream)
        self._stdout_handle = self._get_std_handle(self.STD_OUTPUT_HANDLE)
        self._stderr_handle = self._get_std_handle(self.STD_ERROR_HANDLE)
        self.default_attributes = self._get_console_info()['attributes']
        self.real_fg = self.default_attributes & 0x7
    
    def display(self, codes=[], fg=None, bg=None):
        """Displays codes using Windows kernel calls
        """
        codes, fg, bg = Magic.displayformat(codes, fg, bg)
        color = 0
        for c in codes:
            try:
                f = getattr(self, '_display_' + c)
                out = f()
                if out: color |= out
            except AttributeError:
                pass
        cfg, cfgi, cbg, cbgi = self._split_attributes(
                          self._get_console_info()['attributes'])
        if self.reverse_input:
            cfg, cbg = (cbg // 0x10), (cfg * 0x10)
            cfgi, cbgi = (cbgi // 0x10), (cfgi * 0x10)
        if fg != None:
            color |= self.FG[fg]
            self.real_fg = self.FG[fg]
        else: color |= cfg
        if bg != None:
            color |= self.BG[bg]
        else: color |= cbg
        color |= (cfgi | cbgi)
        fg, fgi, bg, bgi = self._split_attributes(color)
        if self.dim_output:
            # intense black
            fg = 0
            fgi = self.FG_INTENSITY
        if self.reverse_output:
            fg, bg = (bg // 0x10), (fg * 0x10)
            fgi, bgi = (bgi // 0x10), (fgi * 0x10)
            self.reverse_input = True
        if self.hidden_output:
            fg = (bg // 0x10)
            fgi = (bgi // 0x10)
        self._set_attributes(fg | fgi | bg | bgi)
    
    def get_size(self):
        """see doc in Term class"""
        attr = self._get_console_info()
        cols = attr['window']['right'] - attr['window']['left'] + 1
        lines = attr['window']['bottom'] - attr['window']['top'] + 1
        return cols, lines
    
    def _get_std_handle(self, handleno):
        """Returns a handle from GetStdHandle
        
        handleno is one of:
        * self.STD_OUTPUT_HANDLE for stdout
        * self.STD_ERROR_HANDLE for stderr
        """
        #TODO: is NotImplemented the proper way to do this?
        return NotImplemented
    
    def _get_console_info(self):
        """Get information from GetConsoleScreenBufferInfo
        
        Returns a dictionary with the following keys::
        
            max size
            position
            window
            attributes
            size
        
        Note: the y part of size is misleading
        """
        return NotImplemented
    
    def _clear_console(self, length, start):
        """Clears a part of the console
        
        Has a similar effect as writing out spaces.
        
        length: int length of cleared section
        start : tuple of x and y coords to start at
        """
        return NotImplemented
    
    def _set_attributes(self, code):
        """ Set console attributes with `code`
        
        Not implemented here. To be implemented by subclasses.
        """
        return NotImplemented
    
    def _split_attributes(self, attrs):
        """Spilt attribute code
        
        Takes an attribute code and returns a tuple containing
        foreground (fg), foreground intensity (fgi), background (bg), and
        background intensity (bgi)
        
        Attributes can be joined using ``fg | fgi | bg | bgi``
        """
        fg = attrs & self.FG_ALL
        fgi = attrs & self.FG_INTENSITY
        bg = attrs & self.BG_ALL
        bgi = attrs & self.BG_INTENSITY
        return fg, fgi, bg, bgi
    
    def _undim(self):
        self.dim_output = False
        if self.reverse_input:
            a = self._get_console_info()['attributes'] & 0x8f
            self._set_attributes( (self.real_fg * 0x10) | a)
        else:
            a = self._get_console_info()['attributes'] & 0xf8
            self._set_attributes(self.real_fg | a)
    
    def _display_default(self):
        self.hidden_output = False
        self.reverse_output = False
        self.reverse_input = False
        self.dim_output = False
        self.real_fg = self.default_attributes & 0x7
        self._set_attributes(self.default_attributes)

    def _display_bright(self):
        self._undim()
        return self.FG_INTENSITY
    
    def _display_dim(self):
        self.dim_output = True
    
    def _display_reverse(self):
        self.reverse_output = True
    
    def _display_hidden(self):
        self.hidden_output = True
    
    def _get_position(self):
        """Set the cursor's current position
        
        Returns a tuple in the form (x, y)
        """
        pos = self._get_console_info()['position']
        return pos['x'], pos['y']
    
    
    def _set_position(self, coord):
        """Set the cursor's position
        
        coord is a tuple in the form (x, y)
        """
        return NotImplemented
    
    def move(self, place, distance = 1):
        """see doc in Term class"""
        x, y = self._get_position()
        if place == 'up':
            y -= distance
        elif place == 'down':
            for i in range(distance): print
            nx, ny = self._get_position()
            y = ny
            self.move('beginning of line')
        elif place == 'left':
            x -= distance
        elif place == 'right':
            x += distance
        elif place == 'beginning of line':
            x = 0
        elif place == 'beginning of screen':
            x = 0
            y = self._get_console_info()['window']['top']
        else:
            raise ValueError("invalid place to move")
        self._set_position((x, y))
    
    def clear(self, scope = 'screen'):
        """see doc in Term class
        
        According to http://support.microsoft.com/kb/99261 the best way
        to clear the console is to write out empty spaces
        """
        #TODO: clear attributes too
        if scope == 'screen':
            bos = (0, self._get_console_info()['window']['top'])
            cols, lines = self.get_size()
            length = cols * lines
            self._clear_console(length, bos)
            self.move('beginning of screen')
        elif scope == ' beginning of line':
            pass
        elif scope == 'end of line':
            curx, cury = self._get_position()
            cols, lines = self.get_size()
            coord = (curx, cury)
            length = cols - curx
            self._clear_console(length, coord)
        elif scope == 'end of screen':
            curx, cury = self._get_position()
            coord = (curx, cury)
            cols, lines = self.get_size()
            length = (lines - cury) * cols - curx
            self._clear_console(length, coord)
        elif scope == 'line':
            curx, cury = self._get_position()
            coord = (0, cury)
            cols, lines = self.get_size()
            self._clear_console(cols, coord)
            self._set_position((curx, cury))
        elif scope == 'left':
            self.move('left')
            self.write(' ')
        elif scope == 'right':
            self.write(' ')
            self.move('left')
        else:
            raise ValueError("invalid scope to clear")
        
    def getch(self):
        """Don't use this yet
        
        It doesn't belong here but I haven't yet thought about a proper
        way to implement this feature and the features that will depend on
        it.
        """
        return NotImplemented
        return self.msvcrt.getch()
    
    def bell(self):
        self.stream.write('\x07')

class Win32Term(WinTerm):
    """PyWin32 version of Windows terminal control.
    
    Uses the PyWin32 Libraries <http://sourceforge.net/projects/pywin32/>.
    
    ActiveState has good documentation for them:
    
    Main page:
    http://aspn.activestate.com/ASPN/docs/ActivePython/2.4/pywin32/PyWin32.html
    Console related objects and methods:
    http://aspn.activestate.com/ASPN/docs/ActivePython/2.4/pywin32/PyConsoleScreenBuffer.html
    """
    
    def __init__(self, stream):
        import win32console
        self.win32console = win32console
        WinTerm.__init__(self, stream)
    
    def set_title(self, name):
        return self.win32console.SetConsoleTitle(name)
    
    def _get_console_info(self):
        # example output from GetConsoleScreenBufferInfo
        # {'MaximumWindowSize': PyCOORDType(X=80,Y=82),
        # 'CursorPosition': PyCOORDType(X=0,Y=6),
        # 'Window': PySMALL_RECTType(Left=0,Top=0,Right=79,Bottom=24),
        # 'Attributes': 7,
        # 'Size': PyCOORDType(X=80,Y=300)}
        attrs = self._stdout_handle.GetConsoleScreenBufferInfo()
        return {'max size': self._pyCoord_dict(attrs['MaximumWindowSize']),
                'position': self._pyCoord_dict(attrs['CursorPosition']),
                'window': self._pySMALL_RECTType_dict(attrs['Window']),
                'attributes': attrs['Attributes'],
                # y part of size value is misleading
                'size': self._pyCoord_dict(attrs['Size']) }
    
    def _get_std_handle(self, handle):
        return self.win32console.GetStdHandle(handle)
    
    def _get_title(self):
        return self.win32console.GetConsoleTitle()
    
    def _set_attributes(self, attr):
        self._stdout_handle.SetConsoleTextAttribute(attr)
    
    def _set_position(self, coord):
        coord = self.win32console.PyCOORDType(coord[0], coord[1])
        self._stdout_handle.SetConsoleCursorPosition(coord)
        
    def _clear_console(self, length, start):
        # length: int
        # start : tuple of x and y coords
        char = unicode(' ')
        coord = self.win32console.PyCOORDType(start[0], start[1])
        # char is unicode
        self._stdout_handle.FillConsoleOutputCharacter(
           char, length, coord)
    
    def _pyCoord_dict(self, coord):
        return { 'x': coord.X, 'y': coord.Y}
    
    def _pySMALL_RECTType_dict(self, rect):
        return { 'left': rect.Left, 'top': rect.Top,
                'right': rect.Right, 'bottom': rect.Bottom}

class WinCTypesTerm(WinTerm):
    """CTypes version of Windows terminal control.
    
    It requires the CTypes libraries <http://sourceforge.net/projects/ctypes/>
    
    As of Python 2.5, CTypes is included in Python by default. User's of
    previous version of Python will have to install it if they what to use
    this.
    """
    
    def __init__(self, stream):
        import ctypes
        self.ctypes = ctypes
        WinTerm.__init__(self, stream)
    
    def set_title(self, name):
        self.ctypes.windll.kernel32.SetConsoleTitleA(name)
    
    def _get_console_info(self):
        # From IPython's winconsole.py, by Alexander Belchenko
        import struct
        csbi = self.ctypes.create_string_buffer(22)
        res = self.ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
                                     self._stdout_handle, csbi)
        (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx,
         maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        return {'max size': {'x':maxx, 'y':maxy },
                'position': {'x':curx, 'y':cury },
                'window': {'left': left, 'top': top,
                           'right': right, 'bottom': bottom},
                'attributes': wattr,
                # y part of size value is misleading
                'size': {'x':maxx, 'y':maxy } }
    
    def _get_std_handle(self, handle):
        return self.ctypes.windll.kernel32.GetStdHandle(handle)
    
    def _get_title(self):
        """According to http://support.microsoft.com/kb/124103 the buffer
        size is 1024
        
        Does not support unicode, only ANSI"""
        #TODO: unicode support
        strbuffer = self.ctypes.create_string_buffer(1024)
        size = self.ctypes.c_short(1024)
        #unicode versions are (Get|Set)ConsolTitleW
        self.ctypes.windll.kernel32.GetConsoleTitleA(strbuffer, size)
        return strbuffer.value
    
    def _set_attributes(self, attr):
        self.ctypes.windll.kernel32.SetConsoleTextAttribute(
                        self._stdout_handle, attr)
    
    def _set_position(self, coord):
        coord = self._get_coord(coord)
        self.ctypes.windll.kernel32.SetConsoleCursorPosition(
                        self._stdout_handle, coord)
        
    def _clear_console(self, length, start):
        # length: int
        # start : tuple of x and y coords
        char = self.ctypes.c_char(' ')
        coord = self._get_coord(start)
        charswritten = self.ctypes.c_int()
        clength = self.ctypes.c_int(length)
        self.ctypes.windll.kernel32.FillConsoleOutputCharacterA(
           self._stdout_handle, char, clength, coord, charswritten)
    
    def _get_coord(self, coord):
        """ It's a hack, see fixcoord in pyreadline's console.py (revision 
        1289)
        """
        x, y = coord
        return self.ctypes.c_int(y << 16 | x)

class Magic(object):
    """Special codes and what not
    
    Don't use these alone
    see http://vt100.net/docs/vt100-ug/chapter3.html
    
    Based on the ANSI X3.64 standard. See http://en.wikipedia.org/wiki/ANSI_X3.64
    """
    ESCAPE = '\x1b'
    CSI = ESCAPE +'['
    OSC = ESCAPE +']'
    # see the reset method
    RESET = ESCAPE + 'c'
    
    
    # pylint: disable-msg=E0602
    DISPLAY = {'default':0, 'bright':1, 'dim':2, 'underline':4, 'blink':5,
             'reverse':7, 'hidden':8 }
    rDISPLAY = dict( (v, k) for k, v in DISPLAY.items())
    # Yellow is a bit weird, xterm and rxvt display dark yellow, while linux
    # and Windows display a more brown-ish color. Bright yellow is always
    # yellow. Order is important here
    COLORS = { 'black':0, 'red':1, 'green':2, 'yellow':3, 'blue':4, 'magenta':5,
               'cyan':6, 'white':7 }
    rCOLORS = dict( (v, k) for k, v in COLORS.items())
    # pylint: enable-msg=E0602
    # TODO: setf from curses uses the colors in a different order for 
    
    @staticmethod
    def displayformat(codes=[], fg=None, bg=None):
        """Makes sure all arguments are valid"""
        if isinstance(codes, basestring):
            codes = [codes]
        else:
            codes = list(codes)
        for code in codes:
            if code not in Magic.DISPLAY.keys():
                raise ValueError("'%s' not a valid display value" % code)
        for color in (fg, bg):
            if color != None:
                if color not in Magic.COLORS.keys():
                    raise ValueError("'%s' not a valid color" % color)
        return [codes, fg, bg]
    
    @staticmethod
    def rdisplay(codes):
        """Reads a list of codes and generates dict
        
        >>> Magic.rdisplay([])
        {}
        >>> result = Magic.rdisplay([1,2,34,46])
        >>> sorted(result.keys())
        ['bg', 'codes', 'fg']
        >>> sorted(result['codes'])
        ['bright', 'dim']
        >>> result['bg']
        'cyan'
        >>> result['fg']
        'blue'
        """
        dcodes = []
        fg = bg = None
        for code in codes:
            code = int(code)
            offset = code // 10
            decimal = code % 10
            if offset == 3 and decimal in Magic.COLORS.values(): fg = decimal
            elif offset == 4 and decimal in Magic.COLORS.values(): bg = decimal
            elif code in Magic.DISPLAY.values(): dcodes.append(code)
            else: pass # drop unhandled values
        r = {}
        if len(codes): r['codes'] = [Magic.rDISPLAY[c] for c in dcodes]
        if fg != None: r['fg'] = Magic.rCOLORS[fg]
        if bg != None: r['bg'] = Magic.rCOLORS[bg]
        return r

    @staticmethod
    def display(codes=[], fg=None, bg=None):
        codes, fg, bg = Magic.displayformat(codes, fg, bg)
        codes = [str(Magic.DISPLAY[code]) for code in codes]
        if fg != None: codes.append(str(30 + Magic.COLORS[fg]))
        if bg != None: codes.append(str(40 + Magic.COLORS[bg]))
        return Magic.CSI + ";".join(codes) + 'm'

def display(codes=[], fg=None, bg=None):
    """Returns an ANSI display code. This is useful when writing to an Term
        
    codes
        A list containing strings. The strings should one of the keys in
        ``Magic.DISPLAY``. It can also be just a single string.
    fg, bg
        A string. Explicitly for setting the foreground or background. Use
        one of the keys in ``Magic.COLORS``.
        
    .. code-block:: python
    
        # give bright blue foreground and white background with underline
        display(('bright','underline'),'blue','white')
        # gives a blue foreground
        display(fg='blue')
        # resets the color to the default.
        display('default')
    
    Avoid using black or white. Depending on the situation the default
    background/foreground is normally black or white, but it's hard to
    tell which. Bare terminals are normally white on black, but virtual
    terminals run from X or another GUI system are often black on white.
    This can lead to unpredicatble results. If you want reversed
    colours, use the 'reverse' code, and if you want to set the
    colors back to their original colors, use the 'default' code.
    
    Also, be prudent with your use of 'hidden' and 'blink'. Several terminals
    do not support them (and for good reason too), they can be really
    annoying and make reading difficult.
    """
    return Magic.display(codes, fg, bg)

# try to use the Windows method first because their are some terminals on
# MS Windows that support both the Windows and curses methods, but their
# curses implementations are buggy.

def _get_terms():
    terms = None
    if 'win32' in sys.platform or 'cygwin' == sys.platform:
        terms = _get_term(WinCTypesTerm) or _get_term(Win32Term)
    if not terms:
        terms = (_get_term(CursesTerm) or 
                 _get_term(UnixTerm) or 
                 _get_term(Term))
    return terms

def _get_term(termclass):
    try:
        return (termclass(sys.stdin), termclass(sys.stdout),
                termclass(sys.stderr))
    except ImportError: return None

stdin, stdout, stderr = _get_terms()
