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

"""Input and output functions
"""

import sys
import os
import os.path
import term
from term import stdout, stderr, display

__all__ = ["input_object","query","file_chooser"]

# this constant is here because float() and int() give error messages
# that would confuse most sane users.

ERROR_MESSAGE = ( display('bright','red') + 'Error: ' + display('default') +
                 '%s' + '\a' + os.linesep )
NICE_INPUT_ERRORS = {
    float: "The input ('%s') must be a number",
    int: "The input ('%s') must be an integer (-1, 0, 1, 2, etc.)"
}

DEFAULT_INPUT_ERRORS = "Bad input (%s)"

def input_object(prompt_text, cast = None, default = None,
                 prompt_ext = ': ', castarg = [], castkwarg = {}):
    """Gets input from the command line and validates it.
    
    prompt_text
        A string. Used to prompt the user. Do not include a trailing
        space.
        
    prompt_ext
        Added on to the prompt at the end. At the moment this must not
        include any control stuff because it is send directly to
        raw_input
        
    cast
        This can be any callable object (class, function, type, etc). It
        simply calls the cast with the given arguements and returns the 
        result. If a ValueError is raised, it
        will output an error message and prompt the user again.

        Because some builtin python objects don't do casting in the way
        that we might like you can easily write a wrapper function that
        looks and the input and returns the appropriate object or exception.
        Look in the cast submodule for examples.
        
        If cast is None, then it will do nothing (and you will have a string)
        
    default
        function returns this value if the user types nothing in. This is
        can be used to cancel the input so-to-speek
        
    castarg, castkwarg
        list and dictionary. Extra arguments passed on to the cast.
    """
    while True:
        stdout.write(prompt_text)
        value = stdout.raw_input(prompt_ext)
        if value == '': return default
        try:
            if cast != None: value = cast(value, *castarg, **castkwarg)
        except ValueError as details:
            if cast in NICE_INPUT_ERRORS: # see comment above this constant
                stderr.write(ERROR_MESSAGE % (NICE_INPUT_ERRORS[cast] % details))
            else: stderr.write(ERROR_MESSAGE % (DEFAULT_INPUT_ERRORS % str(details)))
            continue
        return value

def query(question, values, default=None, list_values = False, ignorecase = True ):
    """Preset a few options
    
    The question argument is a string, nothing magical.
    
    The values argument accepts input in two different forms. The simpler form
    (a tuple with strings) looks like:
    
        .. code-block:: python
        
            ('Male','Female')
    
    And it will pop up a question asking the user for a gender and requiring
    the user to enter either 'male' or 'female' (case doesn't matter unless
    you set the third arguement to false).
    The other form is something like:
    
        .. code-block:: python
        
            ({'values':('Male','M'),'fg':'cyan'},
            {'values':('Female','F'),'fg':'magenta'})
    
    This will pop up a question with Male/Female (each with appropriate
    colouring). Additionally, if the user types in just 'M', it will be
    treated as if 'Male' was typed in. The first item in the 'values' tuple
    is treated as default and is the one that is returned by the function
    if the user chooses one in that group.
    In addition the function can handle non-string objects quite fine. It
    simple displays the output object.__str__() and compares the user's input
    against that. So the the code
    
        .. code-block:: python
        
            query("Python rocks? ",(True, False))
    
    will return a bool (True) when the user types in the string 'True' (Of
    course there isn't any other reasonable answer than True anyways :P)
    
    ``default`` is the value function returns if the user types nothing in. This is
    can be used to cancel the input so-to-speek
    
    Using list_values = False will display a list, with descriptions printed out
    from the 'desc' keyword
    """
    values = list(values)
    for i in range(len(values)):
        if not isinstance(values[i], dict):
            values[i] = {'values': [values[i]]}
    try:
        import readline, rlcomplete
        wordlist = [ str(v) for value in values
                    for v in value['values']]
        completer = rlcomplete.ListCompleter(wordlist, ignorecase)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer.complete)
    except ImportError:
        pass
    valuelist = []
    for item in values:
        entry = ( display('bright', item.get('fg'), item.get('bg')) +
            str(item['values'][0]) + display(['default']) )
        if str(item['values'][0]) == str(default): entry = '['+entry+']'
        if list_values: entry += ' : ' + item['desc']
        valuelist.append(entry)
    if list_values: question += os.linesep + os.linesep.join(valuelist) + os.linesep
    else: question += ' (' + '/'.join(valuelist) + ')'
    return input_object(question, cast = query_cast, default=default,
                 castarg=[values,ignorecase])

def query_cast(value, answers, ignorecase = False):
    """A cast function for query
    
    Answers should look something like it does in query
    """
    if ignorecase: value = value.lower()
    for item in answers:
        for a in item['values']:
            if ignorecase and (value == str(a).lower()):
                return item['values'][0]
            elif value == a:
                return item['values'][0]
    raise ValueError("Response '%s' not understood, please try again." % value)

def file_chooser(prompt_text = "Enter File: ", default=None, filearg=[], filekwarg={}):
    """A simple tool to get a file from the user. Takes keyworded arguemnts
    and passes them to open().
    
    If the user enters nothing the function will return the ``default`` value.
    Otherwise it continues to prompt the user until it get's a decent response.
    
    filekwarg may contain arguements passed on to ``open()``.
    """
    try:
        import readline, rlcomplete
        completer = rlcomplete.PathCompleter()
        readline.set_completer_delims(completer.delims)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer.complete)
    except ImportError:
        pass
    while True:
        f = raw_input(prompt_text)
        if f == '': return default
        f = os.path.expanduser(f)
        if len(f) != 0 and f[0] == os.path.sep:
            f = os.path.abspath(f)
        try:
            return open(f, *filearg, **filekwarg)
        except IOError as e:
            stderr.write(ERROR_MESSAGE % ("unable to open %s : %s" % (f, e)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
