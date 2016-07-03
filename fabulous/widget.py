"""
    fabulous.widget
    ~~~~~~~~~~~~~~~

    Widget library using terminate.

"""

import os
import math
from datetime import datetime
# import textwrap
from term import stdout, display

class ProgressBar(object):
    """A 3-line progress bar, which looks like::
                                title
        39% [================>----------------------------]
                               message
    
        p = ProgressBar('spam') # create bar
        p.update(0, 'starting spam') # start printing it out
        p.update(50, 'spam almost ready') # progress
        p.update(100, 'spam complete')
    """
    # content, length
    TITLE_FORMAT = {'text':display('bright','cyan') + '%s' + display('default'),
           'length':0,
           'padding':0 }
    BAR_FORMAT = {'text':' %3d%% ' + '[%s'+display('dim')+'%s'+display('default')+']',
           'length':8,
           'padding':2 }
    MESSAGE_FORMAT = {'text': '%s',
           'length': 0,
           'padding': 0 }
        
    def __init__(self, title = None):
        """
        """
        self.drawn = False
        cols = stdout.get_size()[0]
        self.width = cols -1 # TODO: make a better fix for systems that put \n on new line
        self.title = []
        self.barlines = 0
        self.message = []
        self.messageline = None
        self.refresh = False
        self.set_title(title)
    
    def set_title(self, title = None):
        """
        """
        if title == None:
            self.title = []
        else:
            length = self.width - self.TITLE_FORMAT['padding']*2 - self.TITLE_FORMAT['length']
            text = title[:length].center(length) # we need to keep it on one line for now
            padding = ' ' * self.TITLE_FORMAT['padding']
            self.title = [padding + (self.TITLE_FORMAT['text'] % text) + padding]
        self.refresh = self.drawn
            #lines = [(padding + line + padding) for line in textwrap.wrap(
            #          text, self.width - (self.TITLE_FORMAT['padding']*2),
            #          replace_whitespace=False)]
            #self.title = os.linesep.split(
            #          self.TITLE_FORMAT['text'] % os.linesep.join(lines))
    
    def get_title(self):
        """
        """
        return self.title
    
    def get_bar(self, percent):
        """
        """
        barlength = self.width - self.BAR_FORMAT['padding']*2 - self.BAR_FORMAT['length']
        full = int( math.ceil(barlength * (percent / 100.0)) )
        empty = int(barlength - full)
        if full == 0 or empty == 0: fullpiece = ('=' * full)
        else: fullpiece = ('=' * (full-1)) + '>'
        emptypiece = ('-' * empty)
        return [(self.BAR_FORMAT['text'] % (percent, fullpiece, emptypiece))]
    
    def set_message(self, message = None):
        """
        """
        """"""
        if message == None:
            self.message = []
        else:
            length = self.width - self.MESSAGE_FORMAT['padding']*2 - self.MESSAGE_FORMAT['length']
            text = message[:length].center(length) # we need to keep it on one line for now
            padding = ' ' * self.MESSAGE_FORMAT['padding']
            self.message = [padding + (self.MESSAGE_FORMAT['text'] % text) + padding]
    
    def get_message(self):
        """returns None or string"""
        if self.message == []: return None
        else: return os.linesep.join(self.message)
    
    def update(self, percent, message = None, test = False):
        """
        """
        if self.refresh:
            self.clear()
        if self.drawn:
            stdout.move('beginning of line')
            stdout.move('up', len(self.message) + self.barlines)
        else:
            title = self.get_title()
            if title != None:
                for line in self.get_title():
                    stdout.write(line + os.linesep)
            self.drawn = True
        bar = self.get_bar(percent)
        refresh =  (len(bar) != self.barlines)
        self.barlines = len(bar)
        for line in bar:
            stdout.clear('line')
            stdout.write(line)
            stdout.move('down')
            stdout.move('beginning of line')
        if (message != self.get_message()) or refresh:
            stdout.clear('end of screen')
            self.set_message(message)
            for line in self.message:
                stdout.write(line)
                stdout.move('down')
        else: stdout.move('down', len(self.message))
    
    def clear(self):
        """
        """
        if self.drawn:
            stdout.move('beginning of line')
            stdout.move('up', len(self.message))
            stdout.move('up', self.barlines)
            stdout.move('up', len(self.get_title()))
            stdout.clear('end of screen')
            self.drawn = False
        self.refresh = False

class TimedProgressBar(ProgressBar):
    """A 3-line progress bar, which looks like::
                                      title
        39% [================>----------------------------] ETA mm:ss
                                     message
    
        p = ProgressBar('spam') # create bar
        p.update(0, 'starting spam') # start printing it out
        p.update(50, 'spam almost ready') # progress
        p.update(100, 'spam complete')
    """
    
    BAR_FORMAT = {'text':' %3d%% ' + '[%s'+display('dim')+'%s'+display('default')+']',
           'length':13,
           'padding':2 }
    ' ETA 12:23'
    
    # what fraction of percent it acurate too
    precision = 100
    
    def __init__(self, title = None):
        ProgressBar.__init__(self, title)
        self.start = datetime.today()
    
    def get_bar(self, percent):
        now = datetime.today()
        timed = now - self.start
        etatext = ''
        etadiv = int(percent*self.precision)
        if timed.seconds >= 1:
            etatext += ' '
            if int(percent * self.precision) !=0:
                eta = (timed * 100 * self.precision)/int(percent * self.precision)
                days = eta.days
                min, sec = divmod(eta.seconds, 60)
                hours, min = divmod(min, 60)
                if days == 1: etatext += '1 day, '
                elif days: etatext += '%d days, ' % days
                if hours: etatext += '%02d:' % hours
                etatext += '%02d:%02d' % (min, sec)
            else:
                etatext += 'Never'
        barlength = (self.width - self.BAR_FORMAT['padding']*2 
                     - self.BAR_FORMAT['length'] - len(etatext))
        full = int( math.ceil(barlength * (percent / 100.0)) )
        empty = int(barlength - full)
        if full == 0 or empty == 0: fullpiece = ('=' * full)
        else: fullpiece = ('=' * (full-1)) + '>'
        emptypiece = ('-' * empty)
        return [(self.BAR_FORMAT['text'] % (percent, fullpiece, emptypiece))+etatext]

class Spinner(object):
    
    spinners=['/','-','\\','|',]
    
    def __init__(self):
        self.drawn = False
        self.state = 0
    
    def spin(self):
        if self.drawn == True: self.clear()
        else: self.drawn = True
        stdout.write(self.spinners[self.state])
        self.state = (self.state + 1) % len(self.spinners)
        
    def clear(self):
        stdout.clear('left')
        stdout.move('left')
