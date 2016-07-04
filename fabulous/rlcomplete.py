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
    fabulous.rlcomplete
    ~~~~~~~~~~~~~~~~~~~

    Readline related stuff.
"""

import os

class Completer(object):
    """A base class for completers.
    
    Child classes should implement the completelist method.
    """
    text = None
    
    delims = '\t\n'
    
    def __init__(self):
        pass
    
    def complete(self, text, state):
        """The actual completion method
        
        This method is not meant to be overridden. Override the
        completelist method instead. It will make your life much easier.
        
        For more detail see documentation for readline.set_completer
        """
        if text != self.text:
            self.matches = self.completelist(text)
            self.text = text
        try:
            return self.matches[state]
        except IndexError:
            return None

    def completelist(self, text):
        """Returns a list.
        
        The list contains a series of strings which are the suggestions
        for the given string ``text``. It is valid to have no suggestions
        (empty list returned).
        """
        return []

class ListCompleter(Completer):
    """A class that does completion based on a predefined list.
    """
    
    def __init__(self, words, ignorecase):
        self.words = words
        self.ignorecase = ignorecase
    
    def completelist(self,text):
        if self.ignorecase:
            return [w for w in self.words if w.lower().startswith(text.lower())]
        else:
            return [w for w in self.words if w.startswith(text)]


class PathCompleter(Completer):
    """Does completion based on file paths. """
    
    def buildpath(self, base, *paths):
        path = os.path.join(base,*paths)
        if os.path.isdir(os.path.expanduser(path)) and path[-1] != os.path.sep:
            path += os.path.sep
        return path
    
    @staticmethod
    def matchuserhome(prefix):
        """To find matches that start with prefix.
        
        For example, if prefix = '~user' this
        returns list of possible matches in form of ['~userspam','~usereggs'] etc.
        
        matchuserdir('~') returns all users
        """
        if not prefix.startswith('~'):
            raise ValueError, "prefix must start with ~"
        try: import pwd
        except ImportError:
            try: import winpwd as pwd
            except ImportError: return []
        return ['~' + u[0] for u in pwd.getpwall() if u[0].startswith(prefix[1:])]
        
    
    def completelist(self, text):
        """Return a list of potential matches for completion
        
        n.b. you want to complete to a file in the current working directory
        that starts with a ~, use ./~ when typing in. Paths that start with
        ~ are magical and specify users' home paths
        """
        path = os.path.expanduser(text)
        if len(path) == 0 or path[0] != os.path.sep:
            path = os.path.join(os.getcwd(), path)
        if text == '~':
            dpath = dtext = ''
            bpath = '~'
            files = ['~/']
        elif text.startswith('~') and text.find('/', 1) < 0:
            return self.matchuserhome(text)
        else:
            dtext = os.path.dirname(text)
            dpath = os.path.dirname(path)
            bpath = os.path.basename(path)
            files = os.listdir(dpath)
        if bpath =='':
            matches = [self.buildpath(text, f) for f in files if not f.startswith('.')]
        else:
            matches = [self.buildpath(dtext, f) for f in files if f.startswith(bpath)]
        if len(matches) == 0 and os.path.basename(path)=='..':
            files = os.listdir(path)
            matches = [os.path.join(text, f) for f in files]
        return matches
